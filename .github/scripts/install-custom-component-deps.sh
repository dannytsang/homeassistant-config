#!/bin/bash
set -euo pipefail

echo "=== Installing custom component dependencies ==="

# Check for required tools
if ! command -v jq &> /dev/null; then
  echo "❌ Error: jq is not installed. Cannot parse manifest.json files."
  exit 1
fi

python -m pip install --upgrade pip

echo "Processing custom component manifests..."

total_components=0
components_with_deps=0
components_without_deps=0
failed_components=()
installed_reqs=()

for manifest in custom_components/*/manifest.json; do
  if [ -f "$manifest" ]; then
    component=$(basename "$(dirname "$manifest")")
    total_components=$((total_components + 1))
    echo "📦 Processing: $component"

    requirements=$(jq -r '.requirements[]? // empty' "$manifest" 2>/dev/null || echo "")
    if [ -n "$requirements" ]; then
      components_with_deps=$((components_with_deps + 1))
      echo "  Installing: $requirements"

      while IFS= read -r req; do
        [ -n "$req" ] && installed_reqs+=("$component :: $req")
      done <<< "$requirements"

      if echo "$requirements" | xargs -n1 pip install; then
        echo "  ✅ Successfully installed all dependencies"
      else
        echo "  ⚠️  Warning: Some dependencies failed to install for $component"
        failed_components+=("$component")
      fi
    else
      components_without_deps=$((components_without_deps + 1))
      echo "  ℹ️  No requirements found"
    fi
  fi
done

echo ""
echo "=== Summary ==="
echo "Total components: $total_components"
echo "Components with dependencies: $components_with_deps"
echo "Components without dependencies: $components_without_deps"

if [ ${#installed_reqs[@]} -gt 0 ]; then
  echo "Installed requirements:"
  printf '  - %s\n' "${installed_reqs[@]}"
fi

if [ ${#failed_components[@]} -gt 0 ]; then
  echo "⚠️  Components with failed dependencies: ${failed_components[*]}"
else
  echo "✅ All dependencies installed successfully"
fi

if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then
  {
    echo "## 📦 Custom Component Dependency Summary"
    echo ""
    echo "- **Total components scanned:** $total_components"
    echo "- **Components with dependencies:** $components_with_deps"
    echo "- **Components without dependencies:** $components_without_deps"
    echo ""

    if [ ${#installed_reqs[@]} -gt 0 ]; then
      echo "### Installed requirements"
      printf -- '- `%s`\n' "${installed_reqs[@]}"
      echo ""
    fi

    if [ ${#failed_components[@]} -gt 0 ]; then
      echo "### Failed component installs"
      printf -- '- `%s`\n' "${failed_components[@]}"
    else
      echo "✅ All dependency installs completed successfully"
    fi
  } >> "$GITHUB_STEP_SUMMARY"
fi
