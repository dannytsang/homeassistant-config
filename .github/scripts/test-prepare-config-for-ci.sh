#!/bin/bash
set -euo pipefail

repository_root=$(cd -- "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
fixture_dir="$repository_root/.github/tests/prepare-config-for-ci"
config_dir=$(mktemp -d)
output_file=$(mktemp)

cleanup() {
  rm -rf "$config_dir"
  rm -f "$output_file"
}
trap cleanup EXIT

cp -R "$fixture_dir/." "$config_dir/"
(
  cd "$config_dir"
  HA_CHANNEL=stable "$repository_root/.github/scripts/prepare-config-for-ci.sh"
) | tee "$output_file"

if grep -R -q "trigger: device" "$config_dir/packages"; then
  echo "Device trigger was not replaced." >&2
  exit 1
fi

grep -q 'trigger: time' "$config_dir/packages/device_trigger.yaml"
grep -q 'at: "00:00:00"' "$config_dir/packages/device_trigger.yaml"
grep -q '^sonoff:' "$config_dir/configuration.yaml"
grep -q 'Replaced 1 device trigger(s)' "$output_file"

echo "CI preparation regression test passed."
