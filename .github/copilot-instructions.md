<!-- Repo-specific Copilot instructions for this Home Assistant configuration repo -->

# Quick orientation

This repo is a user's Home Assistant configuration: primarily YAML under `packages/`, device firmware under `esphome/`, and local integrations under `custom_components/`. Do not modify `custom_components/` — those are maintained by others.

Focus on small, well-documented changes: add or update a single package, blueprint, or esphome file per PR.

## Key areas
- `packages/` — modular Home Assistant packages (automations, scripts, sensors). Example: `packages/integrations/calendar.yaml`.
- `esphome/` — device firmware YAMLs. Use the `esphome` CLI to compile/upload.
- top-level YAMLs — `configuration.yaml`, `automations.yaml`, `scripts.yaml`, `sensor.yaml`, etc.

## Validation & local checks
- YAML lint: `yamllint .`
- Home Assistant config check (if HA CLI available): `hass --script check_config -c <path-to-config>`
- esphome compile (for changed device files): `esphome compile esphome/<device>.yaml`
- Template testing: use Home Assistant Developer Tools → Templates or run small Jinja checks locally.

## Linting & CI recommendations
- Repo-friendly tools: `yamllint` for YAML, and `pre-commit` for formatting. For Python (only when editing non-maintained code) use `ruff`/`black`.
- Example CI steps to include in PRs: run `yamllint .`, run HA config check, and optionally `esphome compile` for changed files.

## PR checklist (include in PR description)
- Scope summary and motivation.
- Commands you ran: `yamllint .`, `hass --script check_config -c <path>` (or indicate N/A).
- Files changed (avoid `custom_components/`).
- Manual test steps: how to trigger automations or call scripts (see below).

## How to test automations & scripts
- Use Developer Tools → Services to call `script.<name>` or `homeassistant.turn_on` / `automation.trigger`.
- Use Developer Tools → Templates to validate Jinja templates.
- For automation traces, open the automation details in HA and view traces (many automations here use `trace: stored_traces: 20`).

## esphome guidance
- Treat `esphome/` as firmware: changes may require `esphome compile` and device upload. Example: `esphome run esphome/my-device.yaml`.
- Do not assume hardware present when editing; include compile-only validation in CI if possible.

## Blueprints & package conventions
- Add new automations as individual files under `packages/` to keep changes localized. Follow patterns in `packages/integrations/calendar.yaml` (use `sequence:`, `response_variable`, `repeat.for_each`).
- Blueprints belong under `blueprints/` and should include example input definitions and metadata.

## Secrets & backups
- Never commit secrets. Keep using local `secrets.yaml`. Do not modify `secrets.yaml.sample` in the repo.
- Suggest documenting backup steps in PRs when making cross-cutting changes.

## Repo-specific patterns to follow
- Preserve `trace: stored_traces: 20` where traceability is useful.
- Scripts commonly use `response_variable`, templated `message` payloads, and `mode: queued`.

## Merge policy
- Keep PRs small and focused. Include validation commands and a short manual test runbook. Ask the repo owner before any large-scale rename or restructure.

If you'd like, I can add a sample GitHub Actions workflow fragment for CI, or expand any section with exact commands and example PR text.
