#!/bin/bash
# InfluxDB v2 Query Script
# Loads credentials from local .env file - never exposed

set -a
source "$(dirname "$0")/../.env"
set +a

# Arguments
QUERY="${1:-}"
RANGE="${2:--24h}"

if [ -z "$QUERY" ]; then
  echo "Usage: $0 '<flux_query>' [time_range]"
  echo "Example: $0 '|> filter(fn: (r) => r._measurement == \"temperature\")' -7d"
  exit 1
fi

# URL encode the organization name
ORG_ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$INFLUXDB_ORG'''))")

# Execute query with proper Flux headers
curl -s -X POST \
  -H "Authorization: Token $INFLUXDB_TOKEN" \
  -H "Content-Type: application/vnd.flux" \
  -H "Accept: application/csv" \
  "${INFLUXDB_URL}/api/v2/query?org=${ORG_ENCODED}" \
  --data "from(bucket:\"${INFLUXDB_BUCKET}\") |> range(start: ${RANGE}) ${QUERY}"
