[<- Back to Integrations README](../README.md) · [Packages README](../../README.md) · [Main README](../../../README.md)

# Grocy

Consumable stock monitoring and consumption tracking via the [Grocy](https://grocy.info/) inventory management API.

---

## Overview

Two REST sensors poll Grocy for current stock levels of dishwasher tablets and salt blocks. Two REST commands allow Home Assistant to record consumption events directly in Grocy. These are used by kitchen package automations to alert when consumable stock runs low.

---

## Sensors

| Sensor | Entity | Unit | Poll Interval | Grocy Product |
|--------|--------|------|---------------|---------------|
| Dishwasher Tablet Stock | `sensor.dishwasher_tablet_stock` | pcs | 600 s | `input_text.grocy_dishwasher_tablet_product_id` |
| Salt Blocks | `sensor.salt_blocks` | pcs | 600 s | `input_number.grocy_salt_block_product_id` |

Both sensors use `stock_amount_aggregated` from the Grocy stock API response and have `state_class: total`.

---

## REST Commands

| Command | Consumes | Amount |
|---------|---------|--------|
| `rest_command.consume_finish_lemon_dishwasher_tablet` | 1 dishwasher tablet | 1 |
| `rest_command.consume_salt_block` | 1 salt block | 2 |

Both commands POST to the Grocy `/stock/products/{id}/consume` endpoint with `transaction_type: consume` and `spoiled: false`.

---

## Entities Referenced

| Entity | Purpose |
|--------|---------|
| `input_text.grocy_base_url` | Grocy instance base URL |
| `input_text.grocy_dishwasher_tablet_product_id` | Grocy product ID for dishwasher tablets (sensor) |
| `input_number.grocy_finish_lemon_dishwasher_tablet_product_id` | Grocy product ID for dishwasher tablets (REST command) |
| `input_number.grocy_salt_block_product_id` | Grocy product ID for salt blocks |

---

## Dependencies

- **Service:** [Grocy](https://grocy.info/) self-hosted inventory management
- **Secret:** `grocy_api` — Grocy API key
- **Used by:** Kitchen package automations for low-stock alerts

---

*Last updated: 2026-04-05*
