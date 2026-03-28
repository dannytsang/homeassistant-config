#!/bin/bash
set -euo pipefail

echo "=== Preparing Home Assistant config for CI validation ==="

removed_integrations=()
replaced_trigger_count=0

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
removed_integrations+=("battery_notes" "sonoff")

sed -i -e '/battery_notes\:/,+2d' \
       -e '/sonoff\:/,+3d' configuration.yaml

# Additional removals for beta/dev channels
if [ "${HA_CHANNEL:-stable}" != "stable" ]; then
  echo "Removing additional integrations for ${HA_CHANNEL} channel..."
  echo "  - powercalc (compatibility issues with ${HA_CHANNEL})"
  removed_integrations+=("powercalc (${HA_CHANNEL})")
  sed -i -e '/powercalc\:/,+2d' configuration.yaml
fi

# Replace device triggers with dummy time triggers
echo "Replacing device triggers with dummy triggers..."

# Verify packages directory exists
if [ ! -d "packages" ]; then
  echo "⚠️  Warning: packages directory not found, skipping device trigger replacement"
else
  # Count device triggers before replacement
  replaced_trigger_count=$(find packages -name "*.yaml" -type f -exec grep -c "trigger: device" {} + 2>/dev/null | awk '{s+=$1} END {print s}' || echo 0)

  # Replace device triggers
  find packages -name "*.yaml" -type f -exec sed -i \
    -e '/trigger: device$/,/subtype:/c\      - trigger: time\n        at: "00:00:00"  # Dummy trigger for CI validation' {} \;

  echo "  Replaced ${replaced_trigger_count} device trigger(s)"
fi

echo ""
echo "=== Summary ==="
echo "Channel: ${HA_CHANNEL:-stable}"
if [ ${#removed_integrations[@]} -gt 0 ]; then
  echo "Removed integrations: ${removed_integrations[*]}"
else
  echo "Removed integrations: none"
fi
echo "Device triggers replaced: ${replaced_trigger_count}"

echo ""
echo "✅ Config preparation complete"

if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then
  {
    echo "## 🧰 CI Preparation Summary"
    echo ""
    echo "- **Channel:** ${HA_CHANNEL:-stable}"
    if [ ${#removed_integrations[@]} -gt 0 ]; then
      echo "- **Removed integrations:** ${removed_integrations[*]}"
    else
      echo "- **Removed integrations:** none"
    fi
    echo "- **Device triggers replaced:** ${replaced_trigger_count}"
    echo ""
    echo "✅ CI preparation completed successfully"
  } >> "$GITHUB_STEP_SUMMARY"
fi
