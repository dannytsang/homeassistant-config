#!/usr/bin/env python3
"""Install latest stable custom integrations into a disposable HA config."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sys
import tempfile
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import zipfile


API_URL = "https://api.github.com/repos/{repository}/releases/latest"


def request(url: str, token: str | None) -> bytes:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "home-assistant-config-ci",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        with urlopen(Request(url, headers=headers), timeout=60) as response:
            return response.read()
    except (HTTPError, URLError) as err:
        raise RuntimeError(f"Could not download {url}: {err}") from err


def release_for(repository: str, token: str | None) -> dict[str, Any]:
    try:
        release = json.loads(request(API_URL.format(repository=repository), token))
    except json.JSONDecodeError as err:
        raise RuntimeError(f"GitHub returned invalid release metadata for {repository}") from err

    if not isinstance(release, dict) or not release.get("zipball_url"):
        raise RuntimeError(f"No latest stable GitHub release is available for {repository}")
    if release.get("prerelease") or release.get("draft"):
        raise RuntimeError(f"Latest release for {repository} is not a stable release")
    return release


def release_archive_url(release: dict[str, Any]) -> str:
    zip_assets = [
        asset.get("browser_download_url")
        for asset in release.get("assets", [])
        if isinstance(asset, dict)
        and isinstance(asset.get("browser_download_url"), str)
        and str(asset.get("name", "")).endswith(".zip")
    ]
    if len(zip_assets) == 1:
        return zip_assets[0]
    return str(release["zipball_url"])


def component_prefix(archive: zipfile.ZipFile, domain: str) -> PurePosixPath:
    matches = []
    for member in archive.infolist():
        path = PurePosixPath(member.filename)
        if member.is_dir() or path.name != "manifest.json":
            continue
        try:
            manifest = json.loads(archive.read(member))
        except json.JSONDecodeError:
            continue
        if manifest.get("domain") == domain:
            matches.append(path)
    if len(matches) != 1:
        manifests = [
            member.filename
            for member in archive.infolist()
            if PurePosixPath(member.filename).name == "manifest.json"
        ]
        raise RuntimeError(
            f"Expected exactly one manifest for domain {domain!r}; found {len(matches)}. "
            f"Manifest files: {', '.join(manifests) or 'none'}"
        )
    return matches[0].parent


def install_component(
    archive_data: bytes, domain: str, destination: Path
) -> list[str]:
    with tempfile.NamedTemporaryFile(suffix=".zip") as temporary:
        temporary.write(archive_data)
        temporary.flush()
        with zipfile.ZipFile(temporary.name) as archive:
            prefix = component_prefix(archive, domain)
            manifest = json.loads(archive.read((prefix / "manifest.json").as_posix()))
            if manifest.get("domain") != domain:
                raise RuntimeError(
                    f"Manifest domain {manifest.get('domain')!r} does not match {domain!r}"
                )

            target_root = destination / domain
            if target_root.exists():
                shutil.rmtree(target_root)
            target_root.mkdir(parents=True)

            for member in archive.infolist():
                member_path = PurePosixPath(member.filename)
                try:
                    relative_path = member_path.relative_to(prefix)
                except ValueError:
                    continue
                if relative_path == PurePosixPath("."):
                    continue
                if not relative_path.parts or ".." in relative_path.parts:
                    raise RuntimeError(f"Unsafe archive path: {member.filename}")
                target = target_root.joinpath(*relative_path.parts)
                if member.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(member) as source, target.open("wb") as output:
                    shutil.copyfileobj(source, output)

    requirements = manifest.get("requirements") or []
    if not all(isinstance(requirement, str) for requirement in requirements):
        raise RuntimeError(f"Invalid requirements list in {domain} manifest")
    return requirements


def append_summary(resolved: list[dict[str, str]], summary_path: str | None) -> None:
    if not summary_path:
        return
    with Path(summary_path).open("a", encoding="utf-8") as summary:
        summary.write("## External custom integrations\n\n")
        summary.write("Downloaded latest stable GitHub releases into the disposable config.\n\n")
        summary.write("| Domain | Repository | Resolved release |\n")
        summary.write("|---|---|---|\n")
        for item in resolved:
            summary.write(
                f"| `{item['domain']}` | `{item['repository']}` | `{item['release']}` |\n"
            )
        summary.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--config-dir", type=Path, required=True)
    parser.add_argument("--requirements-out", type=Path, required=True)
    parser.add_argument("--resolved-out", type=Path, required=True)
    arguments = parser.parse_args()

    registry = json.loads(arguments.registry.read_text(encoding="utf-8"))
    integrations = registry.get("integrations")
    if not isinstance(integrations, list) or not integrations:
        raise RuntimeError("Registry must contain a non-empty integrations list")

    destination = arguments.config_dir / "custom_components"
    destination.mkdir(parents=True, exist_ok=True)
    token = os.environ.get("GITHUB_TOKEN")
    resolved: list[dict[str, str]] = []
    requirements: set[str] = set()

    for integration in integrations:
        domain = integration.get("domain") if isinstance(integration, dict) else None
        repository = integration.get("repository") if isinstance(integration, dict) else None
        if not isinstance(domain, str) or not isinstance(repository, str):
            raise RuntimeError("Each integration needs string domain and repository fields")
        print(f"Installing {domain} from {repository}")
        release = release_for(repository, token)
        requirements.update(
            install_component(request(release_archive_url(release), token), domain, destination)
        )
        resolved.append(
            {
                "domain": domain,
                "repository": repository,
                "release": str(release.get("tag_name") or release.get("name") or "unnamed"),
            }
        )

    arguments.requirements_out.write_text(
        "".join(f"{requirement}\n" for requirement in sorted(requirements)), encoding="utf-8"
    )
    arguments.resolved_out.write_text(json.dumps(resolved, indent=2) + "\n", encoding="utf-8")
    append_summary(resolved, os.environ.get("GITHUB_STEP_SUMMARY"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as err:
        print(f"ERROR: {err}", file=sys.stderr)
        raise SystemExit(1) from err
