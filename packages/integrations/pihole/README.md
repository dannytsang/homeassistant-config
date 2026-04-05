[<- Back to Integrations README](../README.md) · [Packages README](../../README.md) · [Main README](../../../README.md)

# Pi-hole DNS Ad Filtering

*Last updated: 2026-04-05*

Integrates three Pi-hole instances for network-wide DNS ad filtering. Template sensors aggregate raw per-instance statistics into single house-wide totals. An automation logs any change to filtering status on any instance.

Integration reference: <https://www.home-assistant.io/integrations/pi_hole/>

## Pi-hole Instances

| Switch entity | Instance |
|---------------|----------|
| `switch.pi_hole` | Pi-hole 1 |
| `switch.pi_hole_2` | Pi-hole 2 |
| `switch.pi_holes` | Pi-hole 3 |

## Automations

| Automation | Trigger | Description |
|------------|---------|-------------|
| PiHole: Change Status | Any of the three Pi-hole switches changes state | Logs the instance name and new state (enabled/disabled) to the home log |

## Template Sensors

All sensors aggregate data across all three Pi-hole instances.

| Entity | Aggregation | Unit |
|--------|-------------|------|
| `sensor.pi_hole_total_ads_blocked` | Sum of ads blocked across all 3 instances | ads |
| `sensor.pi_hole_ads_percentage_blocked` | Average blocked percentage across all 3 instances | % |
| `sensor.pi_hole_dns_queries_cached` | Sum of cached queries | queries |
| `sensor.pi_hole_dns_queries_forwarded` | Sum of forwarded queries | queries |
| `sensor.pi_hole_dns_queries_total` | Sum of total DNS queries | queries |
| `sensor.pi_hole_unique_clients` | Sum of unique clients | clients |
| `sensor.pi_hole_unique_domains` | Sum of unique domains | domains |
| `sensor.pi_hole_domains_being_blocked` | Sum of domains on block lists | domains |
| `sensor.pi_hole_seen_clients` | Sum of seen clients | clients |

Each template sensor includes an `availability` expression that returns `unavailable` if any of the three underlying raw sensors is non-numeric, preventing misleading partial totals.

## Notes

- The ads percentage sensor computes the **average** (sum / 3) rather than a sum, since percentage values are not additive.
- Adding or removing a Pi-hole instance requires updating both the switch list in the automation and every template sensor expression.
