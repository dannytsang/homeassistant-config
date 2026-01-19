#!/bin/bash
set -euo pipefail

echo "=== Installing custom component dependencies ==="

python -m pip install --upgrade pip

echo "Processing custom component manifests..."
for manifest in custom_components/*/manifest.json; do
  if [ -f "$manifest" ]; then
    component=$(basename "$(dirname "$manifest")")
    echo "📦 Processing: $component"

    requirements=$(jq -r '.requirements[]? // empty' "$manifest" 2>/dev/null || echo "")
    if [ -n "$requirements" ]; then
      echo "  Installing: $requirements"
      echo "$requirements" | xargs -n1 pip install || echo "  ⚠️  Warning: Some dependencies failed to install"
    else
      echo "  No requirements found"
    fi
  fi
done

echo "✅ Dependency installation complete"
