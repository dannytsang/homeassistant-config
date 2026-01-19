#!/bin/bash
set -euo pipefail

echo "=== Preparing Home Assistant config for CI validation ==="

# Create required directories
echo "Creating required directories..."
mkdir -p camera

# Verify configuration.yaml exists
if [ ! -f "configuration.yaml" ]; then
  echo "❌ Error: configuration.yaml not found"
  exit 1
fi

# Strip problematic integrations from configuration.yaml
echo "Removing integrations that can't validate in CI..."
echo "  - battery_notes (not in base HA image)"
echo "  - sonoff (requires hardware/cloud API)"

sed -i -e '/battery_notes\:/,+2d' \
       -e '/sonoff\:/,+3d' configuration.yaml

# Additional removals for beta/dev channels
if [ "${HA_CHANNEL:-stable}" != "stable" ]; then
  echo "Removing additional integrations for ${HA_CHANNEL} channel..."
  echo "  - powercalc (compatibility issues with ${HA_CHANNEL})"
  sed -i -e '/powercalc\:/,+2d' configuration.yaml
fi

# Replace device triggers with dummy time triggers
echo "Replacing device triggers with dummy triggers..."

# Verify packages directory exists
if [ ! -d "packages" ]; then
  echo "⚠️  Warning: packages directory not found, skipping device trigger replacement"
else
  # Count device triggers before replacement
  device_trigger_count=$(find packages -name "*.yaml" -type f -exec grep -c "trigger: device" {} + 2>/dev/null | awk '{s+=$1} END {print s}' || echo 0)

  # Replace device triggers
  find packages -name "*.yaml" -type f -exec sed -i \
    -e '/trigger: device$/,/subtype:/c\      - trigger: time\n        at: "00:00:00"  # Dummy trigger for CI validation' {} \;

  echo "  Replaced ${device_trigger_count} device trigger(s)"
fi

echo ""
echo "✅ Config preparation complete"
