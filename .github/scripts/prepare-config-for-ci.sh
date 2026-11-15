#!/bin/bash
set -euo pipefail

echo "=== Preparing Home Assistant config for CI validation ==="

replaced_trigger_count=0

# Create required directories
echo "Creating required directories..."
mkdir -p camera

# Verify configuration.yaml exists
if [ ! -f "configuration.yaml" ]; then
  echo "❌ Error: configuration.yaml not found"
  exit 1
fi

echo "External integrations are retained for validation."

# Replace device triggers with dummy time triggers
echo "Replacing device triggers with dummy triggers..."

# Verify packages directory exists
if [ ! -d "packages" ]; then
  echo "⚠️  Warning: packages directory not found, skipping device trigger replacement"
else
  # Count device triggers before replacement
  replaced_trigger_count=$(
    (rg -c --glob "*.yaml" "trigger: device" packages || true) |
      awk -F: '{s+=$NF} END {print s+0}'
  )

  # Replace device triggers. Perl avoids GNU/BSD sed portability differences.
  find packages -name "*.yaml" -type f -exec perl -0pi -e '
    s{^([ \t]*)- trigger: device[ \t]*\n.*?^[ \t]*subtype:[^\n]*\n}
     {$1- trigger: time\n$1  at: "00:00:00"  # Dummy trigger for CI validation\n}gms;
  ' {} +

  echo "  Replaced ${replaced_trigger_count} device trigger(s)"
fi

echo ""
echo "=== Summary ==="
echo "Channel: ${HA_CHANNEL:-stable}"
echo "Removed integrations: none"
echo "Device triggers replaced: ${replaced_trigger_count}"

echo ""
echo "✅ Config preparation complete"

if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then
  {
    echo "## 🧰 CI Preparation Summary"
    echo ""
    echo "- **Channel:** ${HA_CHANNEL:-stable}"
    echo "- **Removed integrations:** none"
    echo "- **Device triggers replaced:** ${replaced_trigger_count}"
    echo ""
    echo "✅ CI preparation completed successfully"
  } >> "$GITHUB_STEP_SUMMARY"
fi
