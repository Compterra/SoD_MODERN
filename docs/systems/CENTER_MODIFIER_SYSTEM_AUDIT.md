# Center Modifier System Audit

## Purpose

The center modifier system is SoD's shared settlement-effect layer. It lets buildings, and later laws, investments, raids, companion actions, or mobile support parties, contribute to one canonical modifier value without every gameplay script needing to know which exact building or source created it.

The system exists and is healthy enough to be the default path for future settlement work. The main remaining polish need is migration discipline: several older systems still check exact `slot_center_has_*` building slots for behavior that should now be expressed as a modifier.

Generated reference reports:

- `docs/reports/center_modifier_system_audit.md`
- `docs/reports/building_system_audit.md`

## Current State

- Registered center modifiers: 61.
- Registered buildings: 29.
- Registry validation issues: 0.
- Building modifier source entries: 116 base derived entries, plus named manual entries from individual buildings.
- Village buildings: 15.
- Town buildings: 13.
- Castle buildings: 8.

The system is centered on three files:

- `src/constants/center_modifier_registry.py`
  - Defines all modifier ids, keys, labels, value types, defaults, and clamps.
  - Maps legacy building `effect_tags` and legacy building fields into center modifiers.
  - Validates modifier ids, bounds, defaults, and value-type rules.

- `src/constants/building_registry.py`
  - Defines building metadata and building-specific `center_modifiers`.
  - Derives modifiers automatically from legacy fields and effect tags.
  - Merges derived and manual modifier entries into each building's final `center_modifiers` tuple.

- `src/scripts/ZI_campaign_ai/sod_center_modifiers.py`
  - Generates `script_sod_get_center_modifier(center, modifier)`.
  - Generates `script_sod_get_center_modifier_totals(center)`.
  - Sums active building modifiers at runtime and clamps the result according to the modifier registry.

## Modifier Categories

### Economy And Trade

Examples:

- `sod_center_modifier_trade_liquidity_flat`
- `sod_center_modifier_trade_volume_pct`
- `sod_center_modifier_market_wealth_flat`
- `sod_center_modifier_production_output_pct`
- `sod_center_modifier_tax_efficiency_pct`

Used by town market, trade demand, economy profile, village output, and prosperity systems.

### Population, Health, And Food

Examples:

- `sod_center_modifier_population_capacity_flat`
- `sod_center_modifier_population_growth_flat`
- `sod_center_modifier_health_cap_flat`
- `sod_center_modifier_health_recovery_flat`
- `sod_center_modifier_food_security_flat`
- `sod_center_modifier_food_consumption_pct`

Used by population supply, health, food limits, food consumption, and construction workforce.

### Security And Recovery

Examples:

- `sod_center_modifier_security_flat`
- `sod_center_modifier_raid_resistance_pct`
- `sod_center_modifier_raid_recovery_flat`
- `sod_center_modifier_threat_reduction_flat`
- `sod_center_modifier_bandit_spawn_reduction_pct`
- `sod_center_modifier_warning_range_flat`
- `sod_center_modifier_patrol_response_pct`

Used by the center security profile, bandit pressure, patrol response, and parts of looter village raid target scoring.

### Military And Recruitment

Examples:

- `sod_center_modifier_infantry_training_flat`
- `sod_center_modifier_ranged_training_flat`
- `sod_center_modifier_cavalry_training_flat`
- `sod_center_modifier_garrison_recovery_flat`
- `sod_center_modifier_garrison_upkeep_pct`
- `sod_center_modifier_troop_upgrade_cost_pct`
- `sod_center_modifier_recruit_count_flat`
- `sod_center_modifier_recruit_tier_bonus_flat`

Used by center military modifier profiles, recruitment, upgrade, garrison recovery, and garrison upkeep systems.

### Construction, Administration, And Prestige

Examples:

- `sod_center_modifier_construction_speed_pct`
- `sod_center_modifier_construction_cost_pct`
- `sod_center_modifier_weekly_upkeep_flat`
- `sod_center_modifier_demesne_cost_flat`
- `sod_center_modifier_renown_weekly_flat`
- `sod_center_modifier_relations_weekly_flat`
- `sod_center_modifier_administration_flat`
- `sod_center_modifier_law_compliance_flat`

Used by construction, building effect totals, support profiles, and administrative economy hooks.

### Faith And Culture

Examples:

- `sod_center_modifier_local_faith_growth_flat`
- `sod_center_modifier_global_faith_growth_flat`
- `sod_center_modifier_faith_stability_flat`
- `sod_center_modifier_cultural_assimilation_flat`

Used by faith drift and faith stability systems.

## Value Semantics

Modifier value types matter.

- `flat`
  - Additive value.
  - Defaults to `0`.
  - Examples: security, population capacity, garrison recovery.

- `percent`
  - Multiplicative value around neutral `100`.
  - Defaults to `100`.
  - Examples: trade volume, construction speed, food consumption.
  - A building entry of `+10` on a percent modifier becomes `110` after default plus building contribution.

- `reduction_percent`
  - Reduction value around neutral `0`.
  - Defaults to `0`.
  - Examples: raid resistance, disease resistance, bandit spawn reduction.
  - Higher is better for reduction, and values are clamped so they cannot reach absurd immunity.

The registry clamps every modifier. This is important because buildings can stack across categories and future sources may stack too.

## Current Consumers

Modifier-driven systems already include:

- `script_sod_get_center_security_profile`
- `script_sod_get_center_food_profile`
- `script_sod_get_center_economy_profile`
- `script_sod_get_center_military_modifiers`
- `script_sod_get_center_population_capacity`
- `script_sod_town_market_profile`
- `script_sod_center_trade_demand_profile`
- `script_sod_village_output_profile`
- `script_sod_get_center_construction_workforce`
- `script_sod_get_center_construction_cost`
- `script_get_center_ideal_health`
- `script_get_center_ideal_prosperity`
- `script_center_get_food_store_limit`
- `script_center_get_food_consumption`
- `script_do_merchant_town_trade`
- `script_update_center_population_supply`

This is enough coverage that new buildings should usually work by declaring modifiers first.

## Hard-Coded Building Slot Consumers

Some direct building checks are still valid. A building can have unique unlock behavior that is intentionally not generic:

- `slot_center_has_prisoner_tower` for prisoner storage and prisoner policy behavior.
- `slot_center_has_chapter` for noble gathering and doctrine-specific behavior.
- `slot_center_has_temple`, `slot_center_has_chapel`, `slot_center_has_monastery`, `slot_center_has_shrine` for explicit faith access or religious event behavior.
- `slot_center_has_barracks`, `slot_center_has_range`, `slot_center_has_stables` for troop upgrade category gates.

Other direct checks are migration candidates because they represent generic effects:

- `process_alarms.py`
  - Watch Tower and Messenger Post should mostly read warning range, security, or patrol response modifiers.

- `update_villages_infested_by_bandits.py`
  - Watch Tower and Messenger Post should mostly read bandit spawn reduction, threat reduction, or warning range modifiers.

- `process_village_raids.py`
  - Watch Tower should mostly read raid resistance and raid recovery modifiers.

- `refresh_village_defenders.py`
  - Watch Tower, Manor, Monastery, Water Supply, Ambulatory, and Clayworks should mostly read garrison recovery, security, health recovery, or raid recovery modifiers.

- `sod_looter_village_raids.py`
  - The looter assault formula already uses `script_sod_get_center_security_profile`, but also manually checks specific buildings for extra defense and loss protection.
  - This should be converted to modifier-driven defense/loss protection before adding many new village defense buildings.

- `change_center_health.py` and `change_center_prosperity.py`
  - These still contain direct building checks. They should gradually move toward health recovery, health cap, prosperity growth, prosperity cap, production, and trade modifiers.

- Weekly building triggers under `src/triggers/ST04_weekly`
  - Many are older one-off building effects. They should be audited one by one and either kept as unique unlocks/events or folded into `get_center_building_effect_totals` and modifier-driven profile scripts.

## Adding Future Buildings

New buildings should be added in this order:

1. Add a save slot constant in `module_constants.py`.
2. Add the slot to the correct building list, such as `village_buildings`, `town_buildings`, or `castle_buildings`.
3. Add a `BUILDING_REGISTRY` entry in `building_registry.py`.
4. Prefer `center_modifiers` and existing legacy fields over new one-off script checks.
5. Only add a direct `party_slot_eq` building check when the building unlocks a unique action, troop type, dialogue branch, or event.
6. Run:
   - `py build\audit_center_modifier_system.py`
   - `py build\audit_building_system.py`
   - `py build\doctor.py --doctor-new-only`
   - `py build\build_all.py`

## Recommended Rule For Buildings

Use modifiers for math.

Use direct building slots for identity.

Examples:

- A Palisade increasing defense should use modifiers like `security_flat`, `raid_resistance_pct`, and `garrison_recovery_flat`.
- A Palisade unlocking a unique "repair palisade stakes" village elder dialogue can use `slot_center_has_palisade`.
- A Militia Yard improving troop recovery should use `garrison_recovery_flat` and `recruit_count_flat`.
- A Militia Yard unlocking a special militia drill scene can use its direct slot.

This keeps systems expandable while preserving room for flavorful building-specific content.

## Optional Future Village Defense Buildings

### Palisade

Suggested modifiers:

- `security_flat +10`
- `raid_resistance_pct +15`
- `garrison_recovery_flat +6`
- `threat_reduction_flat +10`

Deferred for now. A palisade would be mechanically useful, but it asks for visible scene support to feel honest during village assault scenes. Do not add it as a pure stat building until the relevant village scenes can show or imply the works.

### Militia Yard

Suggested modifiers:

- `garrison_recovery_flat +10`
- `recruit_count_flat +1`
- `recruit_tier_bonus_flat +1`
- `security_flat +6`

Direct hooks should be limited to training scenes, militia dialogue, or special local troop availability.

Implemented as `slot_center_has_militia_yard` with modifier-driven garrison recovery, recruit count, recruit tier, security, and raid resistance. It has no scene requirement in v1.

### Beacon Hill

Suggested modifiers:

- `warning_range_flat +1`
- `patrol_response_pct +12`
- `security_flat +4`
- `threat_reduction_flat +8`

Direct hooks should be limited to special reports or emergency warning messages.

Implemented as `slot_center_has_beacon_hill` with modifier-driven warning range, patrol response, security, threat reduction, and light bandit suppression. It has no new scene requirement in v1.

### Granary

Suggested modifiers:

- `food_store_capacity_flat +180`
- `food_security_flat +25`
- `raid_recovery_flat +1`
- `population_recovery_flat +1`

Direct hooks should be rare; most granary behavior should be handled by food and recovery profiles.

Implemented as `slot_center_has_granary` with modifier-driven food storage, food security, raid recovery, population recovery, and migration retention. It has no new scene requirement in v1.

### Militia Armory

Suggested modifiers:

- `recruit_tier_bonus_flat +1`
- `garrison_recovery_flat +4`
- `security_flat +5`
- `raid_resistance_pct +4`

Implemented as `slot_center_has_militia_armory`. It requires either Rustic Blacksmith or Manor, uses small modifier-driven preparedness bonuses, and adds a limited stolen-arms risk when looters win cleanly or overwhelmingly.

## Migration Plan

## Completed Migration

- Village defender refresh now uses `script_sod_get_center_security_profile` and `script_sod_get_center_garrison_policy` for defender target size and post-assault recovery relief.
- Looter village assault math now derives generic defense and loss-protection bonuses from security, raid resistance, patrol response, garrison recovery, health recovery, and food security modifiers.
- Alarm spotting now uses `warning_range_flat` through `script_sod_get_center_security_profile`.
- Village bandit infestation chance and long-range warning messages now use bandit reduction and warning range modifiers.
- Weekly building relation, prosperity, and renown effects now flow through `script_apply_weekly_building_effects`, which reads `script_get_center_building_effect_totals`.
- The Mill, Guild, Prison Tower, University, and Inn weekly triggers now keep unique food, health, random recovery, and message flavor while avoiding duplicate generic relation/prosperity/renown awards.
- The Manor, Stables, and Chapter weekly triggers also no longer apply direct renown/relation awards; their authored stewardship, supply, order, and message flavor remains in place.
- `build/test_center_modifier_migration_static.py` pins the first migration slice.

### Phase 1: Documentation And Guardrails

- Keep `docs/reports/center_modifier_system_audit.md` and `docs/reports/building_system_audit.md` refreshed when buildings change.
- Add a static test that confirms core defense/recovery scripts call modifier profile scripts instead of only checking specific building slots. Done for the first village defense slice in `build/test_center_modifier_migration_static.py`.
- Document allowed exceptions for direct building checks.

### Phase 2: Village Defense Migration

- Convert `refresh_village_defenders.py` to use `script_sod_get_center_garrison_policy` and `script_sod_get_center_security_profile`. Done.
- Convert looter assault building math to read modifier totals first. Done for generic defense/loss-protection math.
- Keep direct checks only for elder flavor dialogue and explicit named-building reports.

### Phase 3: Alarm And Bandit Migration

- Convert `process_alarms.py` to use warning range and patrol response. Warning range conversion done; patrol response is still available through the security profile for future response routing.
- Convert `update_villages_infested_by_bandits.py` to use bandit spawn reduction and threat reduction. Bandit reduction conversion done.
- Confirm Messenger Post and Watch Tower still feel distinct through their modifier profiles.

### Phase 4: Weekly Trigger Cleanup

- Audit each `ST04_weekly` building trigger.
- Keep unique unlock/event effects. Done for Mill, Guild, Prison Tower, University, Inn, Manor, Stables, and Chapter.
- Move generic relation, prosperity, tax, health, renown, and recovery math into modifier profile scripts. Relation, prosperity, and renown are now centralized for the first weekly slice; health/food/recovery flavor remains in legacy triggers where it is still authored as building-specific behavior.

### Phase 5: Expansion

- Add optional future buildings only after the defense/recovery migration is mostly complete.
- Start with Palisade because it has a clear purpose and low conceptual overlap.
- Avoid adding multiple defense buildings until the looter raid system has enough playtest data.

## Risks

- Percent modifiers can be misread. A `percent` modifier defaults to `100`, while `reduction_percent` defaults to `0`.
- Direct slot checks can make new buildings feel dead if scripts never read their modifiers.
- Overlapping defensive buildings can accidentally make villages immune unless clamps and diminishing returns are preserved.
- Generated scripts must be rebuilt after registry changes.
- Some legacy weekly triggers may double-count effects if both the old trigger and a new modifier profile apply the same benefit.

## Conclusion

The modifier system is real, active, and already used by important settlement profiles. It is expandable enough to support future buildings, but the next polish step should be to migrate village defense, alarm, bandit pressure, and recovery scripts away from hard-coded building checks where the effect is generic.

After that migration, adding buildings like Palisade, Militia Yard, Beacon Hill, or Granary becomes mostly a registry/modifier task instead of a web of one-off script edits.
