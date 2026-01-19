#!/bin/bash
set -euo pipefail

echo "=== Preparing Home Assistant config for CI validation ==="

# Create required directories
mkdir -p camera

# Strip problematic integrations from configuration.yaml
echo "Removing integrations that can't validate in CI..."
sed -i -e '/battery_notes\:/,+2d' \
       -e '/a_file_logger\:/,+1d' \
       -e '/openid\:/,+6d' \
       -e '/sonoff\:/,+3d' configuration.yaml

# Additional removals for beta/dev channels
if [ "${HA_CHANNEL:-stable}" != "stable" ]; then
  echo "Removing additional integrations for ${HA_CHANNEL} channel..."
  sed -i -e '/powercalc\:/,+2d' configuration.yaml
fi

# Replace device triggers with dummy time triggers
echo "Replacing device triggers with dummy triggers..."
find packages -name "*.yaml" -type f -exec sed -i \
  -e '/trigger: device$/,/subtype:/c\      - trigger: time\n        at: "00:00:00"  # Dummy trigger for CI validation' {} \;

echo "✅ Config preparation complete"
