# Gameplay Refactor and Optimization Plan

Date: 2026-05-23

## Scope

This report records major gameplay systems that should be considered for refactor or optimization in the Sword of Damocles Modern Mount & Blade 1.011 module-system codebase.

The goal is not to remove features. The goal is to reduce expensive repeated scans, make large trigger blobs easier to reason about, and move old emergency logic into explicit services with stable cadence, cached inputs, and narrow write ownership.

Source fragments are the authority. Expected generated and runtime outputs for most work in this report are:

- Source triggers: `src/triggers/...`
- Source scripts: `src/scripts/...`
- Source mission templates: `src/mission_templates/...`
- Generated Python: `compile/module_simple_triggers.py`, `compile/module_scripts.py`, `compile/module_mission_templates.py`
- Runtime exports: `_export/simple_triggers.txt`, `_export/scripts.txt`, `_export/mission_templates.txt`

Never overwrite live module export files without reviewing the diff first.

## Refactor Principles

- Preserve modular folder ordering and existing trigger order unless the dependency is fully mapped.
- Prefer thin trigger fragments that call named scripts over large inline trigger bodies.
- Keep high-frequency triggers cheap. Avoid broad `try_for_parties`, `try_for_agents`, `try_for_range`, and all-lord/all-center sweeps on every-frame or hourly cadence unless the dataset is intentionally tiny.
- Add dirty flags and cached snapshots when a value is expensive but changes infrequently.
- Keep gameplay writes owned by one stage where possible. A center, party, lord, or companion state should not be rewritten by several unrelated maintenance triggers in the same tick.
- When moving logic, preserve the old behavior first, then optimize in a second pass.
- For new feature text or debug display scratch, prefer `s68` through `s99`.
- Remember that this is M&B 1.011, not Warband. Avoid Warband-only assumptions or operations.

## Priority Summary

| Priority | System | Why it matters | Main risk | Suggested first action |
| - | - | - | - | - |
| 1 | Continuous world-map triggers | Highest-frequency broad sweeps; likely best performance win | Party AI behavior drift | Replace trigger blobs with thin dispatch scripts and dirty flags |
| 2 | Hourly lord AI repair | Large hourly AI maintenance blob with nested lord scans | Campaign AI regressions | Split emergency fixes from normal AI maintenance |
| 3 | Weekly center simulation | Huge weekly economy/population/security fragments with repeated profile calls | Economy balance changes | Introduce one explicit weekly orchestrator that preserves documented order |
| 4 | Trade/caravan/farmer network | All-party scans every 8 hours plus repeated center profile work | Market route balance | Cache center route desirability and process arrivals |
| 5 | Mini-faction world presence | Duplicated faction lifecycle code; Black Khergit response logic is expensive | Spawn pressure balance | Add shared world-presence director with faction hooks |
| 6 | Companion/company/lord morale snapshots | Very large table-shaped systems; repeated party-stack calculations | Narrative and morale side effects | Cache daily/half-day snapshots and table-drive repeated deltas |
| 7 | Prisoner economy | Large logistics layer connected to centers, parties, and pressure systems | Prisoner sale/ransom behavior | Audit daily/weekly entry points before merging with center pipeline |
| 8 | Mission battle preamble | Player-visible battle performance; repeated agent scans | Combat behavior regressions | Cache team/agent state by cadence, then refactor formations carefully |

## 1. Continuous World-Map Trigger Services

### Evidence

Important source fragments:

- `src/triggers/ST01_every_frame/entry_0043.py`
- `src/triggers/ST01_every_frame/entry_0130.py`
- `src/triggers/ST01_every_frame/entry_0052.py`
- `src/triggers/ST01_every_frame/entry_0053.py`
- `src/triggers/ST01_every_frame/entry_0057.py`
- `src/triggers/ST01_every_frame/entry_0175_sod_battle_commander_reset.py`

Observed pressure:

- `entry_0043.py` runs on a `0.1` cadence and loops kingdom heroes. It mixes center arrival, prisoner transfer, garrison adjustment, relation checks, and party XP upgrade work.
- `entry_0130.py` runs on a `0.1` cadence and scans all parties for mercenary or patrol attachment behavior.
- `entry_0052.py` runs on a `0.5` cadence and loops kingdom heroes, then may scan walled centers for avoid-party behavior.
- `entry_0053.py` runs on a `0.5` cadence and scans centers to detect player spotted warnings.
- `entry_0057.py` runs on a zero interval while map-free and calls `script_sod_refresh_player_map_icon`.
- `entry_0175_sod_battle_commander_reset.py` runs on a zero interval and repeatedly checks whether battle commander state needs cleanup.

### Target Shape

Replace the broad continuous sweeps with a small set of named services:

- `script_sod_process_party_arrivals`
- `script_sod_process_attached_service_parties`
- `script_sod_process_lord_avoid_party_ai`
- `script_sod_process_player_spotted_center_warnings`
- `script_sod_refresh_player_map_icon_if_dirty`
- `script_sod_battle_commander_reset_if_dirty`

The trigger files should become thin cadence declarations. The actual work should live in scripts where it can be tested, cached, and reused.

### Optimization Plan

1. Add per-party or per-system latch slots.
   - `slot_party_sod_last_arrival_service_hour`
   - `slot_party_sod_needs_arrival_service`
   - `slot_party_sod_last_attach_service_hour`
   - `slot_center_sod_last_player_spotted_hour`
   - `slot_party_sod_last_avoid_ai_hour`
2. For player map icon refresh, add a global dirty flag such as `$g_sod_player_map_icon_dirty`.
   - Set the dirty flag when camp mode, faction disguise, banner state, or player icon state changes.
   - Replace zero-interval refresh with an `eq, "$g_sod_player_map_icon_dirty", 1` guard.
3. Combine arrival-like behavior from `entry_0043.py` and `entry_0130.py`.
   - Process only parties near or attached to centers.
   - Service garrison/prisoner transfer once per arrival or once per game hour, not every `0.1` tick.
4. Move avoid-party search to hourly or semi-hourly cadence.
   - Cache chosen safe center or last avoid target.
   - Only recompute if the lord remains in the avoid state or the target becomes invalid.
5. Keep compatibility wrappers during migration.
   - First move existing code into scripts without changing cadence.
   - Then reduce cadence and add cache gates after behavior is stable.

### Validation

- Build with the existing build script.
- Diff `compile/module_simple_triggers.py` and `compile/module_scripts.py`.
- Diff `_export/simple_triggers.txt` and `_export/scripts.txt` only after reviewing generated changes.
- Test map travel, center arrivals, lord parties attaching/detaching, patrol/mercenary behavior, camp/break-camp player icon changes, and battle commander cleanup after combat.

## 2. Hourly Lord AI Maintenance

### Evidence

Important source fragments:

- `src/triggers/ST02_every_hour/entry_0027.py`
- `src/triggers/ST02_every_hour/entry_0142.py`
- `src/scripts/ZF_factions/kingdom_hero_decide_next_ai_state.py`
- `src/scripts/ZY_helper_scripts/sod_lord_party_morale.py`

Observed pressure:

- `entry_0027.py` calls `script_process_kingdom_parties_ai` every 2 hours.
- `entry_0142.py` runs every hour and appears to have started as a negative-gold fix, but now includes self-war cleanup, lord-party repair, commander relationship checks, garrison transfer, retreat handling, and repeated calls into AI state calculation.
- The hourly maintenance path scans lords and centers in ways that overlap with normal kingdom-party AI.

### Target Shape

Split the current hourly maintenance into explicit services:

- `script_sod_fix_kingdom_self_wars`
- `script_sod_fix_lord_negative_gold`
- `script_sod_refresh_lord_commander_cache`
- `script_sod_process_lord_garrison_recovery`
- `script_sod_repair_invalid_lord_ai_states`
- `script_sod_assign_lord_retreat_target`

Normal AI should remain owned by `script_process_kingdom_parties_ai` and related campaign-AI scripts. Repair scripts should only touch invalid or stale state.

### Optimization Plan

1. Separate emergency fixes from normal behavior.
   - Negative-gold and self-war cleanup can remain simple, cheap guards.
   - Garrison transfer and retreat target search should not live in the same block.
2. Cache commander relationships.
   - Instead of every lord scanning every other lord hourly, update a commander/follower cache when AI state or party attachment changes.
   - Store a direct commander party or troop slot where practical.
3. Cache retreat targets.
   - A lord in retreat should select a safe center once, then reuse it until invalid.
   - Recompute only if the center changes faction, is lost, or becomes unreachable.
4. Move garrison recovery to an arrival or state-change service.
   - If a lord is in a center and eligible to recover troops, process once per center stay or once per day.
5. Keep `entry_0142.py` as a thin dispatcher.
   - Use comments naming each maintenance stage.
   - Avoid embedding large loops in the trigger fragment.

### Validation

- Build and diff generated simple triggers/scripts.
- Create a save with several kingdoms at war and observe lord AI for several days.
- Check lords retreating after defeat, lords recovering troops in centers, marshal/follower parties, and kingdom self-war cleanup.
- Confirm the normal `script_process_kingdom_parties_ai` cadence still runs.

## 3. Weekly Center Simulation Pipeline

### Evidence

Important source fragments:

- `docs/reports/center_tick_dependency_map.md`
- `src/scripts/ZY_helper_scripts/sod_center_simulation_pipeline.py`
- `src/triggers/ST04_weekly/entry_0018.py`
- `src/triggers/ST04_weekly/entry_0019.py`
- `src/triggers/ST04_weekly/entry_0038.py`
- `src/triggers/ST04_weekly/entry_0104.py`
- `src/triggers/ST04_weekly/entry_0105.py`
- `src/triggers/ST04_weekly/entry_0107.py`
- `src/triggers/ST04_weekly/entry_0123.py`
- `src/triggers/ST04_weekly/entry_0160.py`
- `src/triggers/ST04_weekly/entry_0162.py`

Observed pressure:

- The dependency map already defines a 16-stage weekly center order.
- `entry_0104.py` and `entry_0105.py` are very large and repeat source/destination scoring patterns.
- Several weekly stages repeatedly call center profile scripts for security, market, food, capacity, law, health, and construction checks.
- Bounded write helpers exist in `sod_center_simulation_pipeline.py`, but legacy direct helpers still exist in older passes.

### Target Shape

Create one explicit weekly orchestrator while preserving the documented stage order:

- `script_sod_center_weekly_pipeline`
- `script_sod_center_weekly_prepare_profiles`
- `script_sod_center_weekly_apply_population_growth`
- `script_sod_center_weekly_apply_migration`
- `script_sod_center_weekly_apply_security_desperation`
- `script_sod_center_weekly_reconcile_supply`
- `script_sod_center_weekly_apply_construction`
- `script_sod_center_weekly_apply_late_market_and_prisoner_pressure`

The old trigger fragments can initially call these scripts in the same order. Later, they can be collapsed into one weekly trigger only if the ordering contract is fully preserved.

### Optimization Plan

1. Add an explicit center tick context.
   - Cache profile results for the current weekly tick.
   - Suggested slots: security score, food pressure, market score, capacity, health pressure, migration source score, migration destination score.
2. Warm profiles once per center.
   - `sod_center_security_profile` already has daily caching, but weekly simulation can still avoid repeated calls inside one tick.
   - Goods, food, capacity, and construction inputs should be prepared once and reused.
3. Extract migration scoring.
   - Replace duplicated village/town source/destination blocks with helper scripts.
   - Suggested helpers:
     - `script_sod_center_get_migration_source_score_to_reg`
     - `script_sod_center_get_migration_destination_score_to_reg`
     - `script_sod_center_transfer_weekly_migrants`
4. Extract desperation scoring.
   - Use one helper for the common pressure model and pass center type as data.
   - Keep village/town/castle differences as parameters or small branch blocks.
5. Route writes through bounded helpers.
   - Prefer `script_sod_center_apply_population_delta`, `script_sod_center_transfer_population`, `script_sod_center_apply_wealth_delta`, and related bounded APIs.
6. Preserve weekly order through small commits.
   - First move code into scripts without changing behavior.
   - Then introduce cached profiles.
   - Then reduce duplicated loops.

### Validation

- Build and diff generated scripts/simple triggers.
- Run or add a center tick dependency audit after each stage.
- Compare center population, food, health, wealth, prosperity, construction, and prisoner pressure before/after a week of simulation.
- Check both towns and villages; castles often use bound-village fallback logic and need explicit coverage.

## 4. Trade, Caravan, and Farmer Network

### Evidence

Important source fragments:

- `src/triggers/ST02_every_hour/entry_0049.py`
- `src/triggers/ST02_every_hour/entry_0050.py`
- `src/scripts/ZY_helper_scripts/sod_trade_network.py`
- `docs/reports/economy_settlements/sod_trade_caravan_system_audit.md`

Observed pressure:

- Caravan and farmer triggers run every 8 hours and scan all parties.
- Arrival, tax, tariff, food, prosperity, security, and route-choice work are mixed in trigger bodies.
- `sod_trade_network.py` is large and calls other center profile systems.

### Target Shape

Move toward an arrival-driven trade service:

- `script_sod_trade_process_caravan_arrival`
- `script_sod_trade_process_farmer_arrival`
- `script_sod_trade_refresh_center_route_cache`
- `script_sod_trade_select_cached_route`
- `script_sod_trade_apply_market_exchange`

The trigger should find eligible parties cheaply and call one service. Route quality should be cached by center or refreshed on a daily cadence, not recalculated deeply by every moving party.

### Optimization Plan

1. Cache route desirability by center.
   - Refresh once per day or when center ownership/security/market state changes.
   - Store best nearby destinations, risk score, and expected margin.
2. Process arrivals, not all active travel.
   - If a caravan/farmer is not at a center and does not need rerouting, skip quickly.
3. Consolidate repeated tax and food formulas.
   - Farmer and caravan triggers both touch economic pressure. Move shared arithmetic into scripts.
4. Add last-processed guards.
   - Store the last service hour on the party to prevent repeated processing if a party remains near the same center.
5. Keep market side effects bounded.
   - Use center pipeline helpers where applicable for prosperity, wealth, tariffs, rents, and food deltas.

### Validation

- Compare caravan/farmer route selection over several days.
- Verify tariffs, rents, prosperity, food stores, and center wealth still move.
- Confirm caravans do not stall because a cached destination became invalid.

## 5. Mini-Faction World Presence Director

### Evidence

Important source fragments:

- `src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py`
- `src/scripts/ZY_helper_scripts/sod_elephant_guard_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_jotnar_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_black_army_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_boar_clan_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_serpent_host_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_conquistador_world_presence.py`
- `src/triggers/ST02_every_hour/entry_0159.py`
- `src/triggers/ST03_daily/entry_0158.py`

Observed pressure:

- Several world-presence scripts implement similar lifecycle behavior: scan state, choose pressure area, spawn or update parties, assign AI, and clean stale parties.
- Black Khergit hourly response processing is especially expensive because it can scan responders, threats, defenders, and lord parties.

### Target Shape

Add a shared director and keep flavor-specific scoring in small hooks:

- `script_sod_world_presence_update_faction`
- `script_sod_world_presence_find_origin`
- `script_sod_world_presence_select_target`
- `script_sod_world_presence_spawn_party`
- `script_sod_world_presence_refresh_party_ai`
- `script_sod_world_presence_cleanup_stale_parties`

Faction-specific scripts should answer questions such as "what target is attractive" or "what party template should spawn", not duplicate the entire lifecycle.

### Optimization Plan

1. Define common slots for world-presence factions.
   - Active party count
   - Last spawn day
   - Last response hour
   - Current pressure center
   - Origin party or center
   - Cooldown and escalation level
2. Convert the smallest faction first.
   - Start with a less complex system than Black Khergits.
   - Preserve output behavior, then generalize.
3. Cache Black Khergit threat and responder lists.
   - Refresh every few hours or when a raid is spawned/destroyed.
   - Avoid nested all-defender scans for every threat every hour.
4. Keep spawn balance data close to each faction.
   - Director owns lifecycle.
   - Faction scripts own thresholds, party templates, and target scoring.

### Validation

- Run several in-game weeks and record spawn counts, target centers, raids, and cleanup.
- Confirm no mini-faction stops spawning because a common director branch missed a faction-specific condition.
- Compare Black Khergit raid pressure before and after caching.

## 6. Companion, Company, and Lord Morale Snapshots

### Evidence

Important source fragments:

- `src/scripts/ZY_helper_scripts/sod_companion_depth.py`
- `src/scripts/ZY_helper_scripts/sod_company_accounts.py`
- `src/scripts/ZY_helper_scripts/sod_lord_party_morale.py`
- `src/scripts/ZC_parties/sod_companion_retinues.py`
- `src/triggers/ST02_every_hour/entry_0133.py`
- `src/triggers/ST03_daily/entry_0158.py`

Observed pressure:

- `sod_companion_depth.py` is very large and contains long action-to-companion approval ladders.
- `sod_company_accounts.py` repeatedly computes company wages, due pay, petition candidates, food/supply pressure, and morale effects.
- `sod_lord_party_morale.py` repeatedly walks party stacks for wage and composition estimates, then feeds daily morale and battle willingness logic.

### Target Shape

Introduce snapshot scripts:

- `script_sod_company_accounts_refresh_halfday_snapshot`
- `script_sod_company_accounts_snapshot_is_current_to_reg`
- `script_sod_lord_refresh_daily_party_snapshot`
- `script_sod_lord_get_party_snapshot_value_to_reg`
- `script_sod_companion_apply_action_delta_table`

Snapshots should store expensive derived values once per cadence, then downstream scripts should consume the cached values.

### Optimization Plan

1. Company accounts:
   - At the beginning of the 12-hour company trigger, compute weekly wage, due pay, stack counts, class counts, wounded count, food pressure, and morale bands once.
   - Avoid calling stale-debt and weekly-wage helpers multiple times during the same tick.
2. Lord morale:
   - Compute party size, estimated wage, doctrine composition, supply confidence, fatigue, and morale once per lord per day.
   - Store values in slots and consume them from AI, reports, and battle willingness checks.
3. Companion actions:
   - Replace long repeated per-companion delta ladders with a table-like structure.
   - This can be module-system slots, generated script fragments, or a small dispatcher that only applies non-zero deltas.
4. Companion retinues:
   - Keep identity/flavor text separate from mechanics.
   - Table-drive repeated retinue identity and voice mappings where possible.

### Validation

- Test company pay cycle, debt decay, petition behavior, deserter risk, wounded/supply pressure, and morale report output.
- Test companion approval changes for high-impact actions.
- Test daily lord morale and battle willingness before and after several campaign days.

## 7. Prisoner Economy and Logistics

### Evidence

Important source fragments:

- `src/scripts/ZY_helper_scripts/sod_prisoner_economy.py`
- `src/triggers/ST03_daily/entry_0161.py`
- `src/triggers/ST04_weekly/entry_0162.py`
- `docs/reports/parties_world/prisoner_system_audit.md`
- `docs/reports/parties_world/prisoner_economy_logistics_checklist.md`

Observed pressure:

- The prisoner economy is a large logistics system tied to prisoner trains, center pressure, ransom brokers, slavers, population, economy, and party movement.
- It runs on both daily and weekly cadence.
- It must remain separate from hero-prisoner ransom behavior and player prisoner sale screens.

### Target Shape

Keep prisoner economy as a logistics layer, but make its tick model explicit:

- `script_sod_prisoner_refresh_center_snapshot`
- `script_sod_prisoner_process_daily_trains`
- `script_sod_prisoner_apply_weekly_pressure`
- `script_sod_prisoner_select_train_destination`
- `script_sod_prisoner_apply_arrival_effects`

### Optimization Plan

1. Audit daily and weekly entry points before changing behavior.
2. Cache center prisoner demand/supply once per tick.
3. Coalesce prisoner train nearby-party map-AI scans.
   - A moving train needs nearest hostile, anti-slaver hunter, bandit hunter, and escort candidates.
   - Those should be found by one per-train scan helper, with the decision script consuming cached register outputs instead of looping all parties once per question.
   - Slaver-route anti-slaver center proximity should be folded into the same scan because centers are map parties too.
4. Keep sale/ransom dialogs isolated.
5. Route late center pressure through the center simulation pipeline only after the weekly order is stable.
6. Avoid merging prisoner sale, prisoner trains, hero ransom, and slaver systems into one monolith.

### Validation

- Test prisoner selling to Ramun/guild master/ransom broker paths.
- Test prisoner train creation, routing, arrival, and weekly pressure.
- Check both `strings.txt` and `quick_strings.txt` if changing any prisoner debug or report text.

## 8. Mission and Battle Preamble

### Evidence

Important source fragments:

- `src/mission_templates/_preamble/00_imports.py`
- `src/scripts/ZE_encounters/cf_formation_wedge.py`

Observed pressure:

- The battle preamble is large and includes formation, morale, healthbar, commander duel, and routing logic.
- Several mission behaviors use `try_for_agents` scans.
- `cf_formation_wedge.py` scans agents and ranged weapons for formation checks.

### Target Shape

Refactor battle logic by cadence:

- Spawn-time classification
- Per-second team and morale snapshots
- Formation-command-only recalculation
- Healthbar/display refresh
- Commander duel checks
- Rout/surrender checks

### Optimization Plan

1. Do not start with behavior changes.
   - First split large blocks into named scripts or documented sections.
2. Cache team coherence.
   - Compute once per cadence and reuse in morale/rout/surrender checks.
3. Classify agents on spawn where possible.
   - Store infantry/archer/cavalry/classification data in slots or team-local state.
4. Move formation shape scans to command time.
   - Avoid scanning all agents unless the player or AI actually changes formation.
5. Keep battle regression testing strict.
   - These systems are immediately player-visible.

### Validation

- Test field battles, sieges, routed enemies, healthbars, commander duel behavior, and formation commands.
- Compare battle pacing and morale outcomes before and after.

## Baseline and Instrumentation Work

Before major refactors, add or run lightweight audits so optimization work can be measured:

1. Trigger cadence inventory.
   - Report trigger interval, fragment path, line count, and count of `try_for_parties`, `try_for_agents`, `try_for_range`, `call_script`, and slot operations.
2. Generated operation-size comparison.
   - Compare generated `compile/module_simple_triggers.py`, `compile/module_scripts.py`, and `compile/module_mission_templates.py` before and after each refactor.
3. Runtime scenario checklist.
   - Map travel for 3 days.
   - Kingdom campaign AI for 14 days.
   - Weekly center tick.
   - Caravan/farmer routes.
   - Company payroll.
   - Companion approval event.
   - Prisoner train movement.
   - Field battle with formations.
4. Export diff discipline.
   - Build first.
   - Review generated Python diffs.
   - Review `_export/*.txt` diffs before copying or shipping live module files.

## Recommended Implementation Order

### Phase 0: Baseline

- Run the existing build script.
- Run doctor/static tests already used by the project.
- Generate a trigger/script hotspot report from source fragments.
- Record current generated sizes and key export diffs.

### Phase 1: Cheap High-Frequency Wins

- Refactor `ST01_every_frame` player icon refresh into a dirty-flag service.
- Refactor battle commander reset into a dirty-flag cleanup.
- Move party arrival and attached service-party checks into named scripts without changing cadence.
- Then lower cadence or add last-processed guards.

### Phase 2: Campaign AI Maintenance

- Split `entry_0142.py` into named repair services.
- Cache commander/follower relationships.
- Cache retreat targets.
- Move garrison recovery out of hourly broad sweeps.

### Phase 3: Weekly Center Orchestrator

- Use the existing center tick dependency map as the contract.
- Add weekly center context/profile warmup.
- Extract migration and security desperation scoring.
- Route population/economy writes through bounded helpers.

### Phase 4: Trade and World Presence

- Cache caravan/farmer route desirability.
- Add world-presence director using one smaller mini-faction first.
- Move Black Khergit response logic onto cached threat/responder lists.

### Phase 5: Large Table-Shaped Systems

- Add company half-day snapshot.
- Add lord daily party snapshot.
- Table-drive companion action deltas.
- Keep narrative text and mechanical state separate.

### Phase 6: Battle/Mission Optimization

- Split mission preamble by cadence.
- Cache team coherence and formation classification.
- Validate heavily in live battles.

## Implementation Progress

Completed refactor slices:

- Phase 1 high-frequency world-map services:
  - `ST01_every_frame` arrival, service-party, lord avoid-party, and warning checks now dispatch to named helper scripts.
  - Player map icon refresh is dirty-flagged and no longer runs every frame.
  - Battle commander reset is guarded by a pending flag instead of polling every frame.
  - `ST01_every_frame/entry_0057.py` now delegates the map-icon dirty/initialized/periodic guard to `script_sod_refresh_player_map_icon_if_dirty`.
  - `ST01_every_frame/entry_0175_sod_battle_commander_reset.py` now delegates commander cleanup guard checks to `script_sod_battle_commander_reset_if_dirty`.
  - Kingdom-hero center arrival service cadence was reduced from the legacy `0.1` interval to hourly after extraction, cutting repeated hero sweeps while preserving the same arrival/prisoner/garrison service script.
  - Player mercenary and patrol center-arrival service cadence was reduced from the legacy `0.1` interval to hourly after extraction, cutting repeated all-party sweeps while preserving the same attach/prisoner-transfer service script.
  - Player-spotted center warning service cadence was reduced from half-hourly to hourly after extraction, avoiding duplicate same-hour center sweeps while preserving the same alarm and warning script.
  - `ST02_every_hour/entry_0127.py` now delegates custom-banner world icon propagation to `script_sod_world_map_refresh_custom_banner_parties`; the player map icon is still refreshed every five hours, while the expensive patrol and player-owned-center repaint sweeps run only when the selected custom banner icon changes or the once-per-day safety refresh is due.
  - `ST03_daily/entry_0148.py` now delegates the daily stuck-party position nudge scan to `script_sod_world_map_nudge_stuck_parties`, keeping the trigger thin while preserving the old spawn-point, attached-party, battle-opponent, and old-position guards.
- Phase 2 campaign AI maintenance:
  - `ST02_every_hour/entry_0142.py` now delegates to `script_sod_hourly_lord_ai_maintenance`.
  - Emergency gold/debt repair, self-war repair, commander marking, center-to-lord troop transfer, and retreat target assignment are named services.
  - Lord commander detection now uses a marked slot instead of every lord scanning every other lord.
  - Weak-lord retreat targets are cached for a short window and revalidated before reuse.
  - Center-to-lord troop transfer skips unused garrison math and only reads center stack counts after the transfer path is eligible.
  - `ST03_daily/entry_0032.py` now delegates daily faction-strength recalculation to `script_sod_faction_daily_recalculate_strengths`, keeping the trigger thin while preserving the kingdom loop and existing strength script.
- Phase 3 weekly center pipeline:
  - `ST04_weekly/entry_0104.py` now delegates to `script_sod_center_weekly_apply_migration`.
  - `ST04_weekly/entry_0105.py` now delegates to `script_sod_center_weekly_apply_security_desperation`.
  - Migration and security/desperation remain in the documented dependency-map order.
  - Added `script_sod_center_weekly_store_basic_profile_to_regs` as a fresh per-center weekly profile helper for repeated population/prosperity/health/food/relation reads.
  - The first security/desperation loops now use the shared profile helper instead of duplicating inline food-store and food-consumption math.
  - Added `script_sod_center_weekly_get_migration_food_adjusted_score` so village/town migration paths share the same food scarcity and food capacity scoring rules while preserving the destination-only surplus food bonus.
  - Added `script_sod_center_weekly_get_basic_migration_pressure` for the shared poverty/sickness/unrest pressure baseline.
  - Added `script_sod_center_weekly_get_migration_transfer_to_reg` for the repeated destination-room and score-gap transfer cap.
  - Added `script_sod_center_weekly_get_desperation_scores` so village and walled-center desperation checks share the same hunger, poverty, sickness, unrest, threat, and stability scoring rules.
  - Removed now-redundant per-loop pressure and score initialization from the weekly security/desperation stage.
  - Reused the shared weekly profile helper, migration pressure helper, food-adjusted migration score helper, and transfer-cap helper inside the weekly security/desperation hardship-migration tail.
  - Added shared desperation spawn-chance and bandit-count helpers so village and walled-center bandit outbreak arithmetic no longer duplicate the same chance, pressure, reduction, surplus, and cap math.
  - Added weekly center profile cache slots and refresh/read helpers for the migration stage.
  - `script_sod_center_weekly_apply_migration` now warms center profiles once, reads cached population/prosperity/health/food/relation/lord data during nested destination scans, and updates cached population after each successful transfer.
  - `script_sod_center_weekly_apply_security_desperation` now uses the same warmed center profile cache for desperation checks and hardship migration, with cached population updates after bandit outbreaks and population transfers.
  - `ST03_daily/entry_0034.py` and `ST03_daily/entry_0035.py` now delegate village merchant-inventory refresh and village defender/cattle-flag refresh to `script_sod_village_daily_refresh_merchant_inventories` and `script_sod_village_refresh_defenders_and_cattle_flags`, keeping those maintenance loops in the center/village service layer.
  - `ST03_daily/entry_0051.py` now delegates daily castle food resupply to `script_sod_center_process_daily_castle_food_resupply`, preserving siege exclusion, castle-support inputs, bounded restock capacity, wealth cost, and food-store update behavior.
  - `ST03_daily/entry_0021.py` now delegates the 48-hour kingdom-hero party and garrison training XP pulse to `script_sod_party_process_hero_and_garrison_training_xp`, preserving trainer/player-level scaling, chance gates, battle-opponent guards, and non-player garrison XP behavior.
  - `ST03_daily/entry_0134.py` now delegates the 6-hour player-center trainer XP pulse to `script_sod_center_process_trainer_xp_pulse`, preserving trainer count scaling, troop-type building gates, and the final center upgrade pass while keeping the trigger thin.
- Phase 4 trade and world presence:
  - `ST02_every_hour/entry_0049.py` now delegates kingdom caravan arrival, trade, route-risk, delayed-departure, and reroute handling to `script_sod_trade_network_process_caravan_arrival_tick`.
  - The caravan trigger is now a thin 8-hour dispatcher, leaving route-cache and arrival-service optimization work inside the trade network script instead of trigger glue.
  - `ST02_every_hour/entry_0050.py` now delegates village farmer home/market arrival trade, tariffs, food imports, prosperity/health chance rolls, and return routing to `script_sod_trade_network_process_farmer_arrival_tick`.
  - The farmer trigger is now a thin 8-hour dispatcher beside the caravan trigger, so both trade-party arrival services live in `sod_trade_network.py`.
  - `ST03_daily/entry_0047.py` now delegates daily village-farmer spawn eligibility to `script_sod_trade_network_process_daily_village_farmer_spawn_pulse`, preserving the normal-village gate, stale farmer-party check, 30 percent spawn roll, and slot update.
  - `ST03_daily/entry_0165.py` now delegates daily kingdom-caravan spawn supply to `script_sod_trade_network_process_daily_caravan_spawn_pulse`, keeping active-faction and owned-town gates in the trade-network service layer.
  - Added `script_sod_trade_network_center_allows_departure_to_reg` so caravan and farmer services share one besieged-center departure gate.
  - Added `script_sod_trade_network_send_party_to_center` so caravan and farmer rerouting use one travel-assignment helper, with caravan default-behavior clearing preserved as an explicit parameter.
  - Added daily center departure-profile cache slots for caravan leave-pressure math.
  - Added `script_sod_trade_network_get_center_departure_chance_to_reg`; caravan arrivals now reuse cached prosperity/health/food/population pressure instead of recalculating the same center profile for each caravan at that center on the same day.
  - Added `script_sod_world_presence_configure_activity_party` as the first shared mini-faction world-presence director helper.
  - Jotnar and Elephant Guard world-presence spawns now share the common party faction/base/type/activity setup helper while preserving their separate scoring, spawn cadence, AI behavior, and event messages.
  - Added `script_sod_world_presence_store_slaver_pressure_to_reg` for shared Slaver-market pressure scans.
  - Jotnar and Elephant Guard state updates now use the shared Slaver-pressure helper with their old per-party and near-base weights preserved as parameters.
  - Added `script_sod_world_presence_try_interdict_slaver_to_reg` for shared nearby-Slaver interdiction scans.
  - Jotnar and Elephant Guard daily activity processors now use the shared interdiction helper to assign one eligible patrol/guardian party to attack nearby Slaver traffic while preserving each faction's one-message-per-tick gate.
  - Removed the remaining caller-side Jotnar and Elephant Guard Slaver pre-scans so `script_sod_world_presence_try_interdict_slaver_to_reg` performs the nearby-Slaver scan exactly once per eligible patrol/guardian party.
  - Added cheap active-template gates to Jotnar and Elephant Guard daily processors so days with no active world parties skip village/party activity scans while still refreshing faction state.
  - Added a cheap active-template gate to the Slaver daily transport processor so days with no Slaver transport/recovery parties skip the arrival scan while still refreshing market state.
  - `script_sod_slavers_update_market_state` now returns the active Slaver web-party count in `reg4`, allowing `script_sod_slavers_spawn_world_activity` to reuse the market scan result instead of immediately scanning all parties a second time.
  - Added active-template gates to Boar Clan party setup and center toll-pressure sweeps so zero-band pulses skip work that cannot produce effects, while stale Boar activity cleanup remains unconditional.
  - Added a Black Army activity-present gate around patrol setup, center protection, and road-predator interdiction sweeps; successful same-tick patrol spawns still flip the gate on before the later effect scans run.
  - Added a Serpent Host activity-present gate around route-party setup, walled-center support, and Boar-road shadowing sweeps; successful same-tick route-party spawns still enable the later support and shadowing scans.
  - Added a Conquistador activity-present gate around procurement/camp setup and settlement-support sweeps; successful same-tick logistics spawns still enable the support scan, while independent Slaver/Boar corridor-pressure heat remains ungated.
  - Added weekly merc-market contract income/loss cache slots and changed `script_sod_merc_market_weekly_recover_guilds` to aggregate active contract totals in one party scan before the guild recovery loop, replacing the old per-guild all-party scan.
  - Added a max-bid gate to `script_sod_merc_market_weekly_pulse` so kingdoms with no available bid ceiling skip the nested guild bid-generation loop instead of asking every guild to reject the contract.
  - Gated the final merc-market weekly ledger repair and kingdom-demand refresh behind actual bid generation, so no-bid weeks skip the duplicate cleanup pass while weeks that run guild bid scoring preserve the old post-bid refresh behavior.
  - Removed redundant merc-guild predicate calls from weekly merc-market loops already bounded by `guilds_begin`/`guilds_end`, trimming script dispatch from guild recovery and nested bid scoring without changing the guild set.
  - Removed the same duplicate merc-guild predicate dispatch from preferred-guild selection, guild-ledger overview rendering, and the kingdom/guild weight helper after its direct `guilds_begin`/`guilds_end` range guard.
  - Extended the weekly merc-market contract aggregation with an active contract-value cache and added an optional cached-total path to `script_sod_merc_market_calculate_guild_supply`; weekly bid scoring now reuses the one pre-scan while non-weekly callers keep the live party scan.
  - Added per-kingdom/per-guild weekly contract summary slot ranges for service days, value, losses, and active count; `script_sod_merc_market_calculate_kingdom_guild_weight` can now reuse the weekly pre-scan during bid scoring while normal callers keep the live party scan.
  - Cached weekly guild-supply return values after each guild recovery and refreshed the affected guild cache after accepted bids, so weekly bid scoring no longer recalculates supply for every kingdom/guild pair while later same-pulse bids still see changed capacity.
  - Changed village patrol-demand scoring to pre-count nearby active castle patrols into a temporary village slot from one patrol scan, replacing the old all-party patrol scan inside every eligible village score.
  - Added an active merc-support cache to `script_sod_merc_market_refresh_kingdom_demands`, replacing the per-kingdom all-party support scan during demand refresh while leaving direct demand calculations on the live scan path.
  - Pre-aggregated population-shortage pressure once per demand refresh by center owner and added an optional cached path to kingdom demand calculation, avoiding a full center/profile sweep for every kingdom refresh call.
  - Pre-aggregated lord wealth totals once per demand refresh and reused the cached wealth score in kingdom demand calculation, avoiding a kingdom-hero sweep for every refreshed kingdom.
  - Moved per-kingdom/per-guild contract summary refresh into `script_sod_merc_market_refresh_kingdom_demands` and passed cached totals through preferred-guild selection, avoiding per-guild all-party scans during demand refresh and report refreshes.
  - Made live-path merc-market callers pass explicit zero cache flags to the newly cached helpers, keeping cached totals limited to the optimized weekly and demand-refresh paths.
  - `ST03_daily/entry_0118.py` and `ST03_daily/entry_0120.py` now delegate player and AI mercenary contract expiry checks to `script_sod_merc_process_player_contract_expiry` and `script_sod_merc_process_ai_contract_expiry`, preserving daily trigger ordering while moving the all-party scans into named services.
  - `ST03_daily/entry_0122.py` now delegates daily mercenary reinforcement, player-company replenishment, party XP, and standing perks to `script_sod_merc_process_daily_reinforcement_and_xp`, keeping the trigger thin while preserving the existing daily mercenary maintenance order.
  - `ST03_daily/entry_0129.py` now delegates the 48-hour mercenary lord market pass to `script_sod_merc_process_lord_market_pass`, preserving the kingdom-hero spawn loop, ledger repair, and debug message while removing the inline loop from the trigger.
  - Added `script_sod_world_presence_mark_scan_due_to_reg` as a shared world-presence cadence helper for expensive periodic scans.
  - Black Khergit AI response assignment now uses `slot_faction_black_khergit_last_response_hour` to run the nested threat/responder scan every 3 campaign hours instead of every daytime hour; stale response-target cleanup still runs hourly.
  - Black Khergit camp-response assignment now uses `slot_faction_black_khergit_last_camp_response_hour` so the pressure-65 lord/camp scan runs every 6 campaign hours instead of sharing the anti-raider cadence.
  - Removed a redundant `script_sod_black_khergits_update_horde_state` call from `script_sod_black_khergits_process_ai_responses`; `ST02_every_hour/entry_0159.py` calls the Black Khergit day-cycle immediately before responses, and that day-cycle already refreshes horde state before response slots are read.
  - Moved the Black Khergit pressure-economy horde-state refresh inside its once-per-day gate, so hourly checks no longer rescan horde parties when the daily pressure update is not due.
  - Removed the scout-intelligence horde-state refresh because it is only called from the Black Khergit day-cycle immediately after that cycle refreshes horde state.
  - Removed the immediate day-cycle horde-state refresh after `script_sod_black_khergits_spawn_or_recover_camp`; the spawn/recover step already refreshes horde slots and writes any newly spawned camp party back to the faction slot.
  - Removed the immediate `script_sod_black_khergits_update_horde_state` call from `script_sod_black_khergits_spawn_raids`; the raid script begins with camp spawn/recovery, which already refreshes horde slots before raid decisions are read.
  - Removed duplicate caller-side `script_sod_black_khergits_spawn_or_recover_camp` calls from the weekly pulse and legacy `spawn_bandits` path because `script_sod_black_khergits_spawn_raids` performs that recovery internally.
  - Gated Black Khergit village and caravan harassment sweeps behind the active-raider count, with newly spawned raiders incrementing the local count so same-day raid behavior is preserved while no-raider days skip the nested village/party and raider/caravan scans.
  - Added `slot_faction_black_khergit_last_harassment_day` so duplicate same-day calls to `script_sod_black_khergits_spawn_raids` skip repeated village/caravan harassment sweeps unless that call spawned a new raider.
  - Moved Black Khergit stored-target and target-lock reuse ahead of the town/caravan scoring loop inside `script_sod_black_khergits_update_horde_state`, so valid existing targets skip the nested town scoring and nearby-caravan scan entirely.
  - `script_sod_black_khergits_update_horde_state` now validates `slot_faction_black_khergit_camp_party` first and only falls back to a broad all-party horde-camp search when the stored camp slot is stale.
  - `script_sod_black_khergits_refresh_active_parties` now also validates `slot_faction_black_khergit_camp_party` before doing its preparatory all-party camp lookup, leaving the full normalization pass intact.
  - Reordered cheap siege/enemy gates ahead of Black Khergit target validity checks so target-selection loops avoid Boar-contested-center scans for centers that are already ineligible.
  - Added Black Khergit response scan-token caches for active raider/guard threats and eligible local responders, moving defender eligibility and base-score work out of the per-threat nested scan.
- Phase 5 large table-shaped systems:
  - Added `script_sod_company_accounts_refresh_halfday_snapshot`, a player-party scoped half-day snapshot for weekly wage, paid troop count, class counts, class wages, daily food consumption, edible food count, and food horizon values.
  - `ST02_every_hour/entry_0133.py` now warms the company-account snapshot before the 12-hour company processors run.
  - Wage, food, noble/class count, and class-wage helpers now read the snapshot when it is current and keep their old live calculation paths as compatibility fallbacks.
  - The company accounts report refreshes the snapshot before composing its display so player-facing account details stay current even outside the 12-hour pulse.
  - The daily food-consumption trigger now consumes `script_sod_company_accounts_get_daily_food_consumption_to_regs` instead of recounting player party stacks locally, reusing the snapshot-aware food demand path before the existing ration-pressure and food-removal logic.
  - Added `script_sod_company_accounts_update_ration_pressure_for_food_count`; the daily food trigger now passes the snapshot-aware edible-food count into ration pressure instead of recounting food immediately afterward, while the legacy no-argument helper remains as a compatibility wrapper.
  - Coalesced daily food trigger post-consumption food checks so low-store warning and debug output share one conditional `script_count_edible_food` call instead of counting separately.
  - `script_sod_company_accounts_describe_class_voices_to_s52` now reuses the snapshot-aware class-count helper instead of walking player party stacks again for the company report.
  - Added `script_sod_company_accounts_roster_snapshot_is_current_to_reg`; weekly wage, class-count, and class-wage readers now use the roster-only freshness check so they do not recount edible food when only roster-derived snapshot values are needed.
  - `ST02_every_hour/entry_0124.py` now delegates AI mercenary boss/follower attachment, prisoner drop-off, and return/disband behavior to `script_sod_world_map_process_ai_mercenary_boss_followers`.
  - Added `script_sod_count_active_prisoner_trains_to_regs`; `script_sod_process_prisoner_trains` now refreshes active train counters once and skips train map-AI/reroute/arrival processing on no-train days while preserving center/policy creation paths.
  - Added `script_sod_prisoner_train_scan_nearby_parties_to_regs`; prisoner train map AI now performs one nearby-party scan per train for nearest hostile, nearby anti-slaver center, anti-slaver hunter, bandit hunter, and patrol escort candidates instead of running separate all-party/center scans for each decision.
  - Added cheaper prisoner-train creation gates: capped factions now skip party prisoner-stack scans, patrols from capped factions skip the train-creation helper entirely, and center overcapacity creation skips the pressure recalculation when the center has too few pooled prisoners/laborers to possibly create a train.
  - Added an empty-center gate to weekly prisoner pressure so centers with no pooled prisoners or laborers skip the weekly pressure recalculation entirely.
  - `ST03_daily/entry_0044.py` now delegates hero-prisoner escape checks to `script_sod_prisoner_process_hero_escape_checks`, preserving the main-party roll, walled-center sweep, prisoner-tower chance reduction, and personality modifiers while keeping the trigger thin.
  - `ST03_daily/entry_0060.py` now delegates daily hero-prisoner ransom-offer checks to `script_sod_prisoner_process_daily_ransom_offer`, preserving the rejected-offer gate, main-party check, and early-break scan of player-owned walled centers.
  - `ST03_daily/entry_0149.py` now delegates world-party bloat trimming to `script_sod_trim_bloated_world_parties`, collapsing the old kingdom-hero and hostile-economy cleanup passes into one all-party scan while preserving independent caps and hero-safe removals.
  - Expanded lord-party morale snapshots with daily cached wage, regular count, class percentages/counts, party size, and stack count. Wage/composition helpers now read the current snapshot when valid and fall back by refreshing it.
  - `ST02_every_hour/entry_0029.py` now delegates siege assault/retreat decisions to `script_sod_process_siege_assault_decisions`, isolating the sensitive siege scan for later strength-cache work without changing cadence.
  - Added siege assault attacker-strength caches: `script_sod_siege_refresh_attacker_strength_caches` now makes one kingdom-lord pass and stores attacker strength/marshal presence on each besieged center, so `script_sod_process_siege_assault_decisions` no longer performs a full lord strength scan inside every besieged-center loop.
  - Added `script_sod_center_weekly_get_tax_profile_to_regs`; weekly rents/taxes now consume the weekly center profile cache plus one tax-profile helper instead of scattering population, health, market, extraction, and capacity reads through the trigger.
  - Added `script_sod_center_weekly_apply_rents_and_taxes`; `ST04_weekly/entry_0038.py` is now a thin cadence dispatcher for the full weekly rents/taxes stage.
  - Added `script_sod_companion_apply_core_roster_approval_deltas`; companion action dispatch now applies core-companion deltas through one roster loop instead of sixteen repeated application blocks.
  - `script_cf_party_upgrade_with_xp` now delegates upgrade context resolution, AI training-center fallback selection, stack path resolution, elite caps, permission checks, and single-path application to named helpers. Roaming AI kingdom hero parties can now use a safe lord-owned, faction-central, or faction-owned walled center as their upgrade context before falling back to no-center-safe upgrade rules, while player-facing menus keep their existing center-specific permission checks.
  - The troop upgrade pipeline now has `$g_sod_debug`-gated AI upgrade diagnostics that report context source, center, attempted source/target path, skip reason, upgraded count, and gold spent without touching player-facing upgrade menu behavior.

Validation after these slices:

- `py build\build_all.py`
- `py build\build_all.py --no-cache` after adding the migration profile cache, because the incremental script cache skipped regenerated script output for newly added helper fragments.
- `py build\build_all.py --no-cache` after extracting village merchant and defender maintenance loops.
- `py build\build_all.py --no-cache` after extracting the caravan arrival tick service.
- `py build\build_all.py --no-cache` after extracting the farmer arrival tick service.
- `py build\build_all.py --no-cache` after extracting the daily kingdom-caravan spawn pulse.
- `py build\build_all.py --no-cache` after extracting shared trade departure/routing helpers.
- `py build\build_all.py --no-cache` after adding the caravan departure-profile cache.
- `py build\build_all.py --no-cache` after lowering the two high-frequency world-map arrival service cadences to hourly.
- `py build\build_all.py --no-cache` after lowering the player-spotted center warning service cadence to hourly.
- `py build\build_all.py --no-cache` after gating custom-banner patrol/center repaint sweeps behind icon changes or a daily safety refresh.
- `py build\build_all.py --no-cache` after extracting the daily stuck-party nudge scan.
- `py build\build_all.py --no-cache` after extracting map-icon and battle-commander dirty guard wrappers.
- `py build\build_all.py --no-cache` after adding the shared mini-faction activity-party setup helper.
- `py build\build_all.py --no-cache` after extracting shared Jotnar/Elephant Guard Slaver-pressure scans.
- `py build\build_all.py --no-cache` after extracting shared Jotnar/Elephant Guard Slaver-interdiction scans.
- `py build\build_all.py --no-cache` after removing the remaining caller-side Jotnar/Elephant Guard Slaver pre-scans.
- `py build\build_all.py --no-cache` after adding active-party gates to Jotnar/Elephant Guard daily processors.
- `py build\build_all.py --no-cache` after adding the active-party gate to the Slaver daily transport processor.
- `py build\build_all.py --no-cache` after reusing the Slaver market-state active-party count in weekly Slaver spawning.
- `py build\build_all.py --no-cache` after adding active-party gates to Boar Clan setup and toll-pressure sweeps.
- `py build\build_all.py --no-cache` after adding the Black Army activity-present gate around setup/protection/interdiction sweeps.
- `py build\build_all.py --no-cache` after adding the Serpent Host activity-present gate around setup/support/shadowing sweeps.
- `py build\build_all.py --no-cache` after adding the Conquistador activity-present gate around setup/support sweeps.
- `py build\build_all.py --no-cache` after pre-aggregating weekly merc-market contract income/loss totals by guild.
- `py build\build_all.py --no-cache` after adding the weekly merc-market max-bid gate before guild bid generation.
- `py build\build_all.py --no-cache` after gating the final weekly merc-market repair/refresh pass behind actual bid generation.
- `py build\build_all.py --no-cache` after removing redundant merc-guild predicate calls from guild-bounded weekly merc-market loops.
- `py build\build_all.py --no-cache` after removing duplicate merc-guild predicate dispatch from preferred-guild, overview, and kingdom/guild weight paths.
- `py build\build_all.py --no-cache` after adding the weekly merc-market active contract-value cache and optional cached guild-supply path for bid scoring.
- `py build\build_all.py --no-cache` after adding weekly per-kingdom/per-guild contract summary caches for cached bid-weight scoring.
- `py build\build_all.py --no-cache` after caching weekly guild-supply outputs for bid scoring and refreshing the affected guild cache after accepted bids.
- `py build\build_all.py --no-cache` after replacing per-village patrol-party scans in merc-market village patrol demand with a temporary nearby-patrol count cache.
- `py build\build_all.py --no-cache` after pre-counting active merc-support parties once per demand refresh.
- `py build\build_all.py --no-cache` after pre-aggregating population-shortage pressure once per merc-market demand refresh.
- `py build\build_all.py --no-cache` after pre-aggregating lord wealth once per merc-market demand refresh.
- `py build\build_all.py --no-cache` after pre-aggregating kingdom/guild contract summaries inside merc-market demand refresh and reusing them for preferred-guild selection.
- `py build\build_all.py --no-cache` after making live-path merc-market cache flags explicit.
- `py build\build_all.py --no-cache` after extracting daily player/AI mercenary contract expiry scans into named services.
- `py build\build_all.py --no-cache` after extracting daily mercenary reinforcement/XP maintenance into a named service.
- `py build\build_all.py --no-cache` after extracting the mercenary lord market pass into a named service.
- `py build\build_all.py --no-cache` after adding shared world-presence scan cadence and throttling Black Khergit AI response assignment.
- `py build\build_all.py --no-cache` after splitting Black Khergit threat-response and camp-response cadences.
- `py build\build_all.py --no-cache` after removing the redundant Black Khergit response-side horde-state refresh.
- `py build\build_all.py --no-cache` after removing redundant Black Khergit pressure-economy and scout-intelligence horde-state refreshes.
- `py build\build_all.py --no-cache` after removing the redundant Black Khergit day-cycle horde-state refresh.
- `py build\build_all.py --no-cache` after removing redundant Black Khergit spawn-raid horde refresh and caller-side camp-recovery calls.
- `py build\build_all.py --no-cache` after gating Black Khergit village/caravan harassment scans behind active raiders.
- `py build\build_all.py --no-cache` after adding the Black Khergit daily harassment gate.
- `py build\build_all.py --no-cache` after moving Black Khergit stored-target reuse before town/caravan target scoring.
- `py build\build_all.py --no-cache` after adding stored-camp validation before the Black Khergit all-party camp search.
- `py build\build_all.py --no-cache` after adding stored-camp validation before the Black Khergit active-party refresh camp lookup.
- `py build\build_all.py --no-cache` after reordering Black Khergit target-selection gates ahead of expensive validity checks.
- `py build\build_all.py --no-cache` after caching Black Khergit response threats and responder candidates per response scan.
- `py build\build_all.py --no-cache` after extracting daily faction-strength recalculation into a named service.
- `py build\test_company_accounts_static.py` after adding the company accounts half-day snapshot.
- `py build\test_company_accounts_static.py` after moving daily food demand onto the snapshot-aware helper.
- `py build\test_company_accounts_static.py` after adding the ration-pressure known-food-count helper.
- `py build\test_company_accounts_static.py` after coalescing daily post-consumption food counts.
- `py build\test_company_accounts_static.py` after moving the company voices report onto snapshot-backed class counts.
- `py build\test_company_accounts_static.py` after adding the roster-only company snapshot freshness helper.
- `py build\build_all.py --no-cache` after adding the company accounts half-day snapshot.
- `py build\build_all.py --no-cache` after moving daily food demand onto the snapshot-aware helper.
- `py build\build_all.py --no-cache` after adding the ration-pressure known-food-count helper.
- `py build\build_all.py --no-cache` after coalescing daily post-consumption food counts.
- `py build\build_all.py --no-cache` after moving the company voices report onto snapshot-backed class counts.
- `py build\build_all.py --no-cache` after adding the roster-only company snapshot freshness helper.
- `py build\test_prisoner_economy_static.py` after adding the active prisoner-train gate.
- `py build\test_prisoner_economy_static.py` after coalescing prisoner train nearby-party/anti-slaver-center map-AI scans into one helper.
- `py build\test_prisoner_economy_static.py` after adding cheap prisoner-train creation and patrol-sweep gates.
- `py build\test_prisoner_economy_static.py` after adding the weekly empty-center prisoner-pressure gate.
- `py build\test_prisoner_economy_static.py` after extracting hero-prisoner escape checks into a named service.
- `py build\test_prisoner_economy_static.py` after extracting daily hero-prisoner ransom-offer checks into a named service.
- `py build\test_unique_hero_stack_sources_static.py` after extracting world-party bloat trimming into a single-scan, hero-safe service.
- `py build\test_campaign_party_sanity_static.py` after extracting and gating custom-banner patrol/center repaint sweeps.
- `py build\test_campaign_party_sanity_static.py` after extracting the daily stuck-party nudge scan.
- `py build\test_npc_lord_morale_static.py` after adding daily lord-party wage/composition snapshots.
- `py build\build_all.py --no-cache` after applying the six follow-up refactor slices.
- `py build\build_all.py --no-cache` after extracting weekly rents/taxes into `script_sod_center_weekly_apply_rents_and_taxes`.
- `py build\test_ai_mercenary_clone_regression_static.py` after updating the static guard to validate the current market-pulse architecture.
- `py build\test_companion_depth_system.py` after confirming the companion role dialogue expectation now matches source.
- `py build\test_mercenary_market_static.py` after the AI mercenary validation cleanup.
- `py build\test_mercenary_market_static.py` after extracting daily player/AI mercenary contract expiry scans.
- `py build\test_mercenary_market_static.py` after extracting daily mercenary reinforcement/XP maintenance.
- `py build\test_mercenary_market_static.py` after extracting the mercenary lord market pass.
- `py build\test_unique_hero_stack_sources_static.py` after extracting the mercenary lord market pass.
- `py build\test_feature_audit_static.py` after the AI mercenary validation cleanup.
- `py build\test_town_market_profile.py` after moving the weekly tax logic out of `entry_0038.py`.
- `py build\test_tax_extraction_pressure.py` after moving the weekly tax logic out of `entry_0038.py`.
- `py build\test_population_capacity_limiter.py` after moving the weekly tax logic out of `entry_0038.py`.
- `py build\test_sod_law_static.py` after moving the weekly tax logic out of `entry_0038.py`.
- `py build\test_center_tick_dependency_map.py` after moving the weekly tax logic out of `entry_0038.py`.
- `py build\test_trade_network_static.py` after extracting the daily kingdom-caravan spawn pulse.
- `py build\test_trade_network_static.py` after extracting daily village-farmer spawn eligibility.
- `py build\test_claimant_civil_war_static.py` after extracting daily faction-strength recalculation.
- `py build\test_village_market_recovery.py` after extracting village merchant inventory maintenance.
- `py build\test_village_garrison_unification.py` after extracting village defender/cattle-flag maintenance.
- `py build\test_castle_food_resupply.py` after extracting daily castle food resupply.
- `py build\test_castle_support_profile.py` after extracting daily castle food resupply.
- `py build\test_training_cadence_static.py` after extracting the 48-hour hero-party and garrison training XP pulse into a named service.
- `py build\test_training_cadence_static.py` after extracting the center trainer XP pulse into a named service.
- `py build\test_siege_assault_refactor_static.py` after adding the siege attacker-strength cache.
- `py build\test_npc_lord_morale_static.py` after adding the siege attacker-strength cache.
- `py build\test_siege_capture_resolution_static.py` after adding the siege attacker-strength cache.
- `py build\test_troop_upgrade_pipeline_static.py` after refactoring the troop upgrade pipeline and adding mobile AI lord training-center fallback.
- `py build\test_troop_upgrade_pipeline_static.py` after adding debug-only AI upgrade diagnostics.
- `py build\build_all.py --no-cache` after adding the siege attacker-strength cache.
- `py build\build_all.py --no-cache` after coalescing prisoner train nearby-party/anti-slaver-center map-AI scans into one helper.
- `py build\build_all.py --no-cache` after adding cheap prisoner-train creation and patrol-sweep gates.
- `py build\build_all.py --no-cache` after adding the weekly empty-center prisoner-pressure gate.
- `py build\build_all.py --no-cache` after extracting hero-prisoner escape checks into a named service.
- `py build\build_all.py --no-cache` after extracting daily hero-prisoner ransom-offer checks into a named service.
- `py build\build_all.py --no-cache` after extracting the center trainer XP pulse into a named service.
- `py build\build_all.py --no-cache` after extracting daily village-farmer spawn eligibility.
- `py build\build_all.py --no-cache` after extracting daily castle food resupply.
- `py build\build_all.py --no-cache` after extracting the 48-hour hero-party and garrison training XP pulse into a named service.
- `py build\build_all.py --no-cache` after refactoring the troop upgrade pipeline and adding mobile AI lord training-center fallback.
- `py build\build_all.py --no-cache` after adding debug-only AI upgrade diagnostics.
- `py build\build_all.py --no-cache` after extracting world-party bloat trimming into a single-scan, hero-safe service.
- Doctor: 0 warnings.
- Slot verification: 0 warnings, 0 errors.
- Generated compile import check: OK.
- No live `_export/*.txt` files were overwritten.

Validation cleanup after the follow-up pass:

- The AI mercenary clone regression test now validates `script_sod_merc_market_weekly_pulse`, bid generation, bid acceptance, and `script_cf_spawn_ai_mercs` instead of requiring obsolete inline guild selection inside `script_ai_hire_mercenaries`.
- The companion-depth static test now passes with the current `"Leave the offices as they are."` dialogue text.
- Economy static tests that validate weekly tax behavior now inspect the weekly tax stage as `ST04_weekly/entry_0038.py` plus `sod_center_simulation_pipeline.py`, because the trigger is now intentionally thin.

## Next-Step Audit - 2026-05-24

Question: "What should we do next?"

Proceed status: the first recommendation below, the company accounts half-day snapshot, was implemented on 2026-05-24. A follow-up pass also landed first-slice refactors for the next five targets: AI-mercenary follower extraction, prisoner-train active gating, lord-party daily snapshots, siege-assault extraction, weekly tax-profile centralization, and companion roster-delta application. Later passes extracted the full weekly rents/taxes stage into `script_sod_center_weekly_apply_rents_and_taxes`, cleaned up stale static-test expectations around the mercenary market and tax reports, and added a per-center siege attacker-strength cache to avoid repeated all-lord strength scans.

Audit method:

- Re-read this plan against the completed Phase 1-4 slices.
- Scanned source trigger fragments for remaining `try_for_parties`, `try_for_agents`, `try_for_range`, `call_script`, and distance operations, weighted by cadence.
- Scanned major gameplay scripts for size and loop/call density.
- Cross-checked likely next targets against available static tests and behavioral risk.

Main findings:

- The original Phase 1 high-frequency trigger work is mostly complete. The former `0.1` arrival/attachment/warning services are now thin dispatchers or lower cadence.
- The biggest remaining every-frame scores are guarded Native-style utility triggers, not broad world simulation:
  - `src/triggers/ST01_every_frame/entry_0006.py` is a notification-menu queue drain. It is zero-interval, but guarded by `trp_notification_menu_types` and only loops while a queued menu exists.
  - `src/triggers/ST01_every_frame/entry_0080.py` is cattle-quest progress. It runs at `0.5`, but only when cattle quests are active.
- The remaining high-cadence gameplay trigger worth extracting soon is `src/triggers/ST02_every_hour/entry_0124.py`: it scans all parties hourly for AI mercenary parties owned by kingdom heroes, then handles attachment, prisoner transfer, and return/disband behavior inline.
- The remaining heavy campaign-AI trigger worth treating carefully is `src/triggers/ST02_every_hour/entry_0029.py`: every 3 hours it loops besieged walled centers and repeatedly scans kingdom heroes to decide assault/retreat behavior. It is important, but higher regression risk than the company/prisoner snapshot work.
- The largest script hotspots after the world-presence work are now table-shaped systems:
  - `src/scripts/ZY_helper_scripts/sod_company_accounts.py`: about 3618 lines, 29 range loops, 193 script calls. The 12-hour company trigger calls six company scripts back-to-back, and the same expensive values are recomputed in several places: current weekly wage, due pay, class wages/counts, noble troop counts, daily food consumption, and troop-category morale.
  - `src/scripts/ZY_helper_scripts/sod_prisoner_economy.py`: about 3276 lines, 7 party scans, 17 range loops, 170 script calls. Daily train processing still scans parties and can run nearby threat/hunter/bandit/escort checks per train.
  - `src/scripts/ZY_helper_scripts/sod_lord_party_morale.py`: about 3278 lines, 15 range loops, 71 script calls. It already has party morale snapshots, but daily lord/faction posture work still mixes multiple concerns.
  - `src/scripts/ZY_helper_scripts/sod_companion_depth.py`: about 6094 lines and 324 script calls, but most pressure is table/dispatch complexity rather than broad world scanning.

Recommended next implementation:

1. Build the company accounts half-day snapshot first.
   - Add a `script_sod_company_accounts_refresh_halfday_snapshot` called once at the start of `ST02_every_hour/entry_0133.py`.
   - Cache values already recomputed by several 12-hour/company-report paths: current weekly wage, due pay, pay confidence, camp strain, daily food consumption, edible food count, class wages/counts, noble troop count, and troop-category morale.
   - Keep existing live helper scripts as compatibility wrappers. Add cached read paths gradually so reports and the six 12-hour processors can consume the snapshot without changing behavior.
   - This is the best next slice because it is high code-volume, low world-AI risk, player-party scoped, and has strong existing static coverage in `build/test_company_accounts_static.py`, companion-depth tests, retinue tests, and company-dialogue/menu tests.

2. Then extract the remaining hourly AI-mercenary follower trigger.
   - Move `src/triggers/ST02_every_hour/entry_0124.py` into a named service such as `script_sod_process_ai_mercenary_boss_followers`.
   - Preserve behavior first, then add cheap gates/last-processed slots if the service still proves noisy.
   - This keeps Phase 1 cleanup honest by removing one of the last inline all-party hourly trigger bodies.

3. Then audit and cache prisoner train processing.
   - Status: implemented for the prisoner/slaver/captive pass.
   - `script_sod_process_prisoner_trains` now starts with a prisoner logistics snapshot and gates center overflow, center policy demand, and patrol prisoner-train scans.
   - Destination scoring now uses a same-day prisoner pressure cache before falling back to full center pressure recalculation.
   - Slaver black-market reports/quotes now use cached daily market state, with dirty refresh after transport spawns/removals.
   - Weekly pressure processing remains on the direct recalculation path so weekly consequences stay fresh.
   - Completion audit: the daily path now avoids the old count-then-scan pair, first-day pressure-cache reads cannot use uninitialized slots, and Slaver cache invalidation covers shared party lifecycle paths. Cache-aware market deltas also preserve legitimate same-day Slaver supply/demand effects through a dirty refresh. See `docs/tooling/PRISONER_SLAVER_REFACTOR_AUDIT.md`.

4. Defer the siege assault trigger until after the above.
   - `ST02_every_hour/entry_0029.py` has real performance upside, but it owns sensitive siege timing and marshal assault behavior.
   - Treat it as a dedicated campaign-AI refactor: extract first, then cache besieger party lists/strength by besieged center.

Do not do next:

- More Black Khergit response work unless testing finds a regression. The current response branch now has cadence gates and scan-token caches; the next gains there are smaller and riskier.
- Mission-template battle optimization yet. It is still important, but the player-visible regression risk is higher than company/prisoner snapshot work.
- Broad companion-depth table driving as the immediate next slice. It will improve maintainability, but it is less likely to produce runtime performance wins than company snapshots or prisoner train gates.

## Files Changed By This Audit

Initial audit document:

- `docs/tooling/GAMEPLAY_REFACTOR_OPTIMIZATION_PLAN.md`

Implementation files touched so far:

- `src/triggers/ST01_every_frame/entry_0043.py`
- `src/triggers/ST01_every_frame/entry_0052.py`
- `src/triggers/ST01_every_frame/entry_0053.py`
- `src/triggers/ST01_every_frame/entry_0057.py`
- `src/triggers/ST01_every_frame/entry_0130.py`
- `src/triggers/ST01_every_frame/entry_0175_sod_battle_commander_reset.py`
- `src/triggers/ST02_every_hour/entry_0142.py`
- `src/scripts/ZY_helper_scripts/sod_world_map_trigger_services.py`
- `src/scripts/ZI_campaign_ai/sod_hourly_lord_ai_maintenance.py`
- `src/scripts/ZA_hardcoded_game_scripts/game_start.py`
- `src/scripts/ZC_parties/sod_initialize_party.py`
- `src/scripts/ZE_encounters/sod_battle_commander.py`
- `src/constants/module_constants.py`
- `src/triggers/ST04_weekly/entry_0104.py`
- `src/triggers/ST04_weekly/entry_0105.py`
- `src/scripts/ZY_helper_scripts/sod_center_weekly_migration.py`
- `src/scripts/ZY_helper_scripts/sod_center_weekly_security_desperation.py`
- `src/scripts/ZY_helper_scripts/sod_center_simulation_pipeline.py`
- `src/triggers/ST02_every_hour/entry_0049.py`
- `src/triggers/ST02_every_hour/entry_0050.py`
- `src/scripts/ZY_helper_scripts/sod_trade_network.py`
- `src/scripts/ZY_helper_scripts/sod_world_presence_director.py`
- `src/scripts/ZY_helper_scripts/sod_merc_market_weekly_recover_guilds.py`
- `src/scripts/ZY_helper_scripts/sod_merc_market_weekly_pulse.py`
- `src/scripts/ZY_helper_scripts/sod_jotnar_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_elephant_guard_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_slavers_black_market.py`
- `src/scripts/ZY_helper_scripts/sod_boar_clan_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_black_army_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_serpent_host_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_conquistador_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py`
- `src/triggers/ST04_weekly/entry_0126.py`
- `src/scripts/ZZ_common_array_processing/spawn_bandits.py`
- `src/scripts/ZY_helper_scripts/sod_company_accounts.py`
- `src/triggers/ST02_every_hour/entry_0133.py`
- `src/triggers/ST04_weekly/entry_0038.py`
- `build/test_ai_mercenary_clone_regression_static.py`
- `build/test_town_market_profile.py`
- `build/test_tax_extraction_pressure.py`
- `build/test_population_capacity_limiter.py`
- `build/test_sod_law_static.py`
- `build/test_center_tick_dependency_map.py`
- `build/test_siege_assault_refactor_static.py`
