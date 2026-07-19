# Home Assistant Configuration — Codex Guide

This is the active guidance for Codex when working in this repository. Maintain `claude.md` and `.claude/` independently; do not update them unless the user explicitly asks.

## Repository map

- `configuration.yaml` is the entry point. It loads named packages from `packages/`.
- `packages/rooms/` holds room-specific behaviour. Use it before an integration package when a change belongs to one physical room.
- `packages/integrations/` holds integration-specific behaviour. Root package files hold genuinely global configuration.
- `packages/shared_helpers.yaml` holds shared scripts and templates.
- `automations.yaml`, `scripts.yaml`, and `scenes.yaml` contain UI-managed configuration; do not manually restructure them without an explicit request.
- `esphome/` contains device definitions; `custom_components/` contains checked-in Home Assistant integrations.

Start with [packages/README.md](packages/README.md), then the relevant [rooms overview](packages/rooms/README.md) or [integrations overview](packages/integrations/README.md). Package YAML is the source of truth; the matching README explains local intent.

## Before changing anything

1. Run `git status --short` and preserve unrelated user changes.
2. Read `configuration.yaml`, the target package YAML, its closest README, and any scripts, scenes, helpers, or entities it calls.
3. Search dependencies with `rg` before renaming, removing, or consolidating entities, scripts, scenes, automation IDs, or helpers.
4. Treat entity existence from the live Home Assistant instance as runtime information. Do not call an entity missing merely because it has no YAML definition.
5. Never read, print, create, or commit secrets, credentials, tokens, private camera media, or deployment URLs unless the user explicitly requires it.

## Change rules

- Make the smallest behaviour-complete change. Preserve aliases, automation mode, delays, timeouts, notification/logging paths, manual overrides, and safety behaviour unless the request changes them.
- Use current official Home Assistant documentation for version-sensitive syntax. Local historical notes are not authoritative.
- Use `action:` for service calls. Use singular `response_variable:` when capturing an action response; do not use `response_variables:`.
- Use defensive template defaults such as `| float(0)`, `| int(0)`, or `| default(...)` when entity states or attributes can be unavailable.
- Follow the repository's numeric automation-ID convention and keep IDs unique. It is a local convention, not a Home Assistant schema requirement.
- Use trigger IDs and ordered `choose` branches when combining compatible triggers. First matching `choose` branch wins.
- For motion/presence behaviour, cancel any relevant off/dim timer whenever new presence is detected; do not hide the cancellation in a branch that can be skipped.
- Keep device triggers in source YAML. CI may replace them only in its disposable validation checkout.
- Add or update package documentation only when the externally useful behaviour, setup, dependencies, or inventory changes.

## Automation consolidation

Do not consolidate automations solely because their YAML looks similar. First compare every trigger transition and duration, condition, action order, timer lifecycle, mode, notification, safety path, disabled state, and external caller.

When consolidation is valid:

1. Build a behaviour table for the originals.
2. Preserve a unique existing automation ID where practical.
3. Use trigger IDs and `choose` only where branch precedence is explicit.
4. Remove obsolete YAML and README references only after confirming no callers remain.
5. Compare the final behaviour table to the originals and identify every intentional change.

## Validation

Always inspect `git diff` and run `git diff --check` after an edit. Then use the relevant validation:

- YAML/package/configuration change: Home Assistant configuration check in CI or **Settings → System → Check configuration**.
- Automation/template logic: Developer Tools → Template, plus automation traces after deployment.
- ESPHome change: validate the affected ESPHome YAML; CI validates all device definitions when `esphome/**` changes.
- GitHub workflow change: actionlint in CI.
- Documentation change: verify every edited local link resolves.

CI validates YAML, Markdown, ESPHome, and stable Home Assistant configuration. Beta/dev Home Assistant checks are informational; do not present them as a release guarantee.

## Git and deployment

- Do not commit, push, deploy, reload, restart Home Assistant, or change live state unless explicitly requested.
- Before a requested commit, review the staged diff for credentials and unrelated files. Never add assistant co-author or attribution trailers.
- Keep commit messages concise, imperative, and user-authored.

## Useful references

- [README.md](README.md) — project overview and CI/deployment flow.
- [packages/README.md](packages/README.md) — package architecture and inventory.
- [setup_statistics.md](setup_statistics.md) — YAML-derived counts and current package analysis.
- [statistics.md](statistics.md) — live Home Assistant state snapshot; not a YAML inventory.
- [INSTALL.md](INSTALL.md) — environment-specific setup notes.
