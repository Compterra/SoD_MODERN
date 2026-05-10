# Module System Modernization Checklist

## Goal

Modernize the SoD Module System without a risky big-bang rewrite. The project should remain buildable after every slice, with better safety around old Mount & Blade 1.011 engine edges: dialogue state graphs, encounter exits, invalid party IDs, lord capture flows, menu exports, AI pulses, and large late-game battles.

## Principles

- [ ] Keep every pass small enough to review, test, and build.
- [ ] Prefer central helper scripts over repeated ad hoc operation blocks.
- [ ] Preserve gameplay behavior unless the current behavior is a known bug or unstable engine edge.
- [ ] Use explicit return paths instead of brittle `change_screen_return` when leaving mission/dialogue chains.
- [ ] Validate party, troop, center, faction, quest, and menu context before reading slots.
- [ ] Add static coverage before or alongside risky refactors.
- [ ] Run focused tests, doctor, and a full build after each implementation slice.
- [ ] Do not rewrite generated compile files unless the source of truth lives there.
- [ ] Keep M&B 1.011 limitations in mind; do not assume Warband-only callbacks or operations exist.

## Phase 1: Dialogue And Encounter Safety

### Dialogue Graph Safety

- [x] Audit all dialogue fragments that end in `close_window` and classify whether they need `$g_leave_encounter`, `change_screen_map`, `change_screen_return`, `start_map_conversation`, or no action.
- [x] Add a static dialogue graph check for missing input tokens before full export catches them.
- [x] Add a static dialogue graph check for orphan output states in `src/dialogs`.
- [x] Add a static check for deleted dialogue files still listed in `_order_dialogs.txt`.
- [x] Add a static check for dialogue states that output to stale removed states, especially `*_11`, `*_end`, and old typo-renamed states.
- [x] Add a static check for duplicate player options with identical conditions that can shadow later branches.
- [x] Add a static check for terminal post-battle dialogue branches that do not set `$g_leave_encounter` where required.
- [x] Add a static check for Legion/IEF capture branches that terminate safely after hero death, capture, release, or recruitment.
- [x] Add a static check for `auto_proceed` branches that lead into states with no valid next player option.
- [x] Add a static check for `start_map_conversation` and `change_screen_map_conversation` use outside safe menu contexts.

### Known Dialogue Bug Families

- [x] Jester cheat dialogue no longer routes to battle unless cheat mode is active.
- [x] Honor-duel continue screen exits safely.
- [x] IEF dying Centurion default death reply closes safely.
- [x] Gaius Marcus lore soft-locks are closed safely.
- [x] Removed stale `cpdla_nihilistic_11` order entry.
- [x] Re-audit all `cpdla*` captured Centurion branches after large multi-lord battles.
- [x] Re-audit all `pelha*` surrender/capture branches.
- [x] Re-audit all `legate_sq_*` lore chains for terminal safety.
- [x] Re-audit all lord recruitment, oath, pardon, and rebellion dialogue chains.
- [x] Re-audit companion direct-talk incidents for missing input/output states.

### Encounter Exit Safety

- [x] `game_event_party_encounter` avoids old invalid party reads.
- [x] Stale encounter party IDs are cleared on camp entry.
- [x] Camp entry sanitizes unique hero party stacks.
- [x] Add a shared helper for safe encounter cleanup.
- [x] Replace repeated raw `$g_leave_encounter` assignments with a helper where feasible.
- [x] Audit all mission templates that call `finish_mission` and `jump_to_menu`.
- [x] Ensure `jump_to_menu` happens before `finish_mission` in mission-end triggers where needed.
- [x] Audit menus using `change_screen_return` after mission or conversation exits.
- [x] Add static coverage for unsafe `finish_mission` followed by `jump_to_menu`.
- [x] Add static coverage for generic "Continue" menus that use only `change_screen_return`.

## Phase 2: Party, Troop, And Center ID Safety

### Party Validation

- [x] Late-game `party_calculate_and_set_nearby_friend_strength` invalid `-1` spam fixed.
- [x] AI strength calculation validates active parties before cache updates.
- [x] Unique hero stack sanitizer exists and runs periodically.
- [x] Camp entry invokes unique hero stack sanitizer.
- [x] Create `script_sod_party_is_safe_active_to_reg` or equivalent guard helper if operation support allows it cleanly.
- [x] Audit all `store_distance_to_party_from_party` calls for validated party IDs.
- [x] Audit all `store_faction_of_party` calls for validated party IDs.
- [x] Audit all `party_get_slot` and `party_slot_eq` calls using globals like `$g_encountered_party`, `$current_town`, `$g_enemy_party`, `$g_talk_troop_party`.
- [x] Audit all `str_store_party_name` calls using faction slots or globals that can be `-1`.
- [x] Add static checks for unguarded `store_distance_to_party_from_party` in high-frequency triggers/scripts.
- [x] Add static checks for unguarded `$g_encountered_party` party operations.

### Troop And Hero Validation

- [x] Prisoner selling rejects heroes and non-soldier troops.
- [x] Prisoner transfer paths reject non-soldier hero stacks.
- [x] Unarmed troop prisoner crash path has guards.
- [x] Audit all `party_force_add_prisoners` calls for hero and troop range safety.
- [x] Audit all `party_add_members` calls that can add unique heroes to non-leader stacks.
- [x] Audit lord death, capture, release, recruit, oath, and faction-change paths.
- [x] Add static checks for hero prisoner movement without explicit intended hero handling.
- [x] Add static checks for duplicate hero stack risks outside debug-only menus.

### Center Validation

- [x] Audit all `script_get_closest_center` consumers for `reg0` validation.
- [x] Audit all center report menus that display faction-slot target centers.
- [x] Add fallback strings for missing or invalid target centers in mini-faction reports.
- [x] Add static checks for `str_store_party_name` after faction target-center slot reads without center range checks.
- [x] Add static checks for village/castle/town operations using `:center` from script output without `is_between`.

## Phase 3: Menus, Reports, And Presentation Safety

### Menu Export Reliability

- [x] Recent `menus.txt` unexpected EOF issue prompted line-break auditing.
- [x] Hardcoded M&B 1.011 presentation/script mapping warnings investigated.
  - [x] Add static menu export shape checks for line-break-sensitive generated menu records.
  - [x] Add static checks for menu option condition/action bracket balance before export.
  - [x] Add static checks for menu IDs referenced by `jump_to_menu`.
  - [x] Add static checks for menus with only one `Continue` option that cannot leave safely.
  - [x] Add static checks for camp/report menus that evaluate high-risk scripts in option conditions.

### Report Safety

  - [x] Audit all camp reports for invalid party/faction/center slots.
  - [x] Audit all report actions with cooldown globals for stale state.
  - [x] Add safe default text for unavailable mini-faction targets.
  - [x] Add safe default text for unavailable invasion front centers.
  - [x] Add safe default text for unavailable quest focus centers/parties.
  - [x] Add static coverage for report menus that call description scripts.

### Presentation Safety

  - [x] Audit custom presentations for M&B 1.011 availability.
  - [x] Remove or gate Warband-only hardcoded presentation names.
  - [x] Add static test for `prsnt_game_start` and `prsnt_game_escape` absence in the M&B 1.011 presentation order.
  - [x] Add notes documenting any intentionally omitted hardcoded presentation/script callbacks.

## Phase 4: Campaign AI Modernization

### AI Pulse Safety

- [x] Nearby friend/enemy strength calculation refactored and guarded.
  - [x] Audit every script called by the 7-hour AI simple trigger.
  - [x] Audit every script called by daily AI triggers.
  - [x] Audit every script called by weekly AI triggers.
  - [x] Add cadence comments to high-frequency scripts.
  - [x] Add static checks for high-frequency scripts that call unsafe party operations.
  - [x] Split large AI scripts into smaller helpers where it reduces repeated state reads.

### Lord AI And Diplomacy

  - [x] Centralize faction personality reads.
  - [x] Centralize AI war/peace/truce memory updates.
  - [x] Centralize lord campaign posture calculations.
  - [x] Centralize IEF aggression rules and mercenary restrictions/allowances.
  - [x] Add static checks that IEF remains expansionist and hostile as designed.
  - [x] Add static checks for kingdom_6-only hero death rules.

### Battle And Formation AI

- [x] Formation `J` key no longer conflicts with `Ctrl+J`.
- [x] Formation reset clears stale scripted order state.
- [x] Enemy reinforcement dismount behavior was reviewed/fixed.
  - [x] Audit all mission template formation injections for consistency.
  - [x] Add static checks that formation reset is included in major battle mission templates.
  - [x] Audit ammo/restock behavior for multi-wave battles.
  - [x] Audit battle morale integration for troop categories.

## Phase 5: Quest Framework Modernization

### Quest Registration

- [x] Quest terminal sentinel loads last.
- [x] Keep quest end sentinel in its own file and last in order.
- [x] Audit quest files for runtime metadata completeness.
- [x] Add static checks for missing quest framework IDs in companion personal arcs.
- [x] Add static checks for quest journal text that distinguishes â€œtalk to companionâ€ from â€œgo to place/actor.â€

### Runtime And Journal

- [x] Centralize quest accept/update/complete/fail calls in helper surfaces.
- [x] Audit `sod_quest_runtime_accept`, `sod_quest_runtime_update`, `sod_quest_runtime_complete`, and `sod_quest_runtime_fail` usage.
- [x] Audit `sod_quest_dialogue_record_event` usage.
- [x] Audit `sod_quest_journal_update` usage.
- [x] Audit `sod_quest_outcome_apply_consequences` usage.
- [x] Add static checks for companion arcs with no recorded memory event.
- [x] Add static checks for quests with no outcome consequences.

## Phase 6: Companion And Incident Modernization

### Companion Depth

- [x] Companion approval framework exists.
- [x] Companion campfire exists.
- [x] Companion role framework exists.
- [x] Many companion incident surfaces exist.
- [x] Move remaining camp-only incidents toward direct dialogue/adventure surfaces.
- [x] Ensure each companion arc has focus center, focus party, or focus cause where appropriate.
- [x] Ensure each companion arc has journal hints that name the place/actor when relevant.
- [x] Ensure each companion arc has at least one companion-at-site comment where appropriate.
- [x] Add static checks for missing companion quest framework migration targets.

### Shared Gameplay Hooks

- [x] Centralize companion reaction dispatch for slavery, mercy, raids, diplomacy, IEF actions, Black Khergit tribute, trade contracts, and company morale.
- [x] Add static checks for major systems calling companion action hooks.
- [x] Add static checks that warning/reconciliation branches exist before departure logic.
- [x] Add static checks for companion direct-talk pending incident entries.

## Phase 7: Mini-Faction Modernization

### World Presence

- [x] Slavers have Black Market Web world presence.
- [x] Jotnar have Hearthbound Kin world presence.
- [x] Elephant Guard have Sacred Warden world presence.
- [x] Black Khergits have Moving Horde world presence.
- [x] Boar Clan has toll/frontier pressure.
- [x] Serpent Host has route intelligence.
- [x] Black Army has road-security presence.
- [x] Centralize mini-faction pressure descriptors.
- [x] Centralize mini-faction target-center validation.
- [x] Centralize mini-faction player countermeasure cooldowns.
- [x] Add static checks for mini-faction party templates with missing encounter dialogue.
- [x] Add static checks for mini-faction reports with invalid target fallback text.

### Cross-Faction Reactions

- [x] Audit all mini-faction cross-references for valid slots and factions.
- [x] Add dispatch helpers for cross-faction incidents.
- [x] Add static checks for Slaver/Jotnar/Elephant Guard anti-slavery reaction links.
- [x] Add static checks for Black Khergit/Boar/Serpent/Black Army road-pressure links.

## Phase 8: Economy, Trade, And Company Systems

### Trade Network

- [x] Caravan dialogue intelligence exists.
- [x] Trade network report exists.
- [x] Caravan memory slots exist.
- [x] Audit caravan origin/destination slots for invalid party IDs.
- [x] Add safe fallbacks for missing caravan destinations.
- [x] Add static checks for caravan dialogue calling trade description helpers.
- [x] Centralize route risk and mini-faction pressure reads.

### Company Accounts And Morale

- [x] Manual payday foundation exists.
- [x] Ration policy exists.
- [x] Recreation exists.
- [x] Troop-category morale split exists.
- [x] Battle promise and post-battle morale consequences exist.
- [x] Audit troop dialogue incidents for terminal safety.
- [x] Add static checks for mutiny/desertion dialogue closure paths.
- [x] Add static checks for company incident focus party/center/cause.
- [x] Audit in-battle morale hooks for high-risk mission-template contexts.

## Phase 9: Builder, Doctor, And Tooling

### Build Pipeline

- [x] Fragment builders exist for scripts, dialogs, menus, quests, simple triggers, mission templates, and presentations.
- [x] Doctor report exists.
- [x] Add doctor checks for dialogue graph input/output validity.
- [x] Add doctor checks for unsafe post-mission `change_screen_return`.
- [x] Add doctor checks for unguarded high-frequency party operations.
- [x] Add doctor checks for missing M&B 1.011 hardcoded callback compatibility notes.
- [x] Add doctor checks for stale files listed in `_order_*.txt`.
- [x] Add doctor checks for duplicate menu/dialog IDs where unsafe.

### Static Tests

- [x] Create `build/test_modernization_static.py` as a top-level modernization guard.
- [x] Add modernization test coverage for dialogue graph safety.
- [x] Add modernization test coverage for encounter exit safety.
- [x] Add modernization test coverage for high-frequency AI party safety.
- [x] Add modernization test coverage for camp/report invalid target fallbacks.
- [x] Add modernization test coverage for quest sentinel/order safety.
- [x] Add modernization test coverage for M&B 1.011 callback compatibility.

### Developer Workflow

- [x] Root note documents `rg.exe` environment issue.
- [x] Add a `docs/reports/modernization_status.md` generated or manually updated after major passes.
- [x] Keep a "recently fixed old bugs" section in this checklist.
- [x] Add a "known launcher/tooling oddities" section documenting arbitrary `py` invocation access issues.
- [x] Prefer approved build commands for verification.

## First Implementation Slice: Dialogue + Encounter Safety

- [x] Add `build/test_modernization_static.py`.
- [x] Check dialogue order references point to existing files.
- [x] Check dialogue outputs have matching input states or are safe terminal states.
- [x] Check no dialogue references removed `cpdla_nihilistic_11`.
- [x] Check generic continue menus do not rely only on `change_screen_return`.
- [x] Check mission templates do not call `finish_mission` before `jump_to_menu`.
- [x] Check `game_event_party_encounter` remains inert/safe for invalid party IDs.
- [x] Check camp entry clears stale encounter parties and sanitizes unique hero stacks.
- [x] Check IEF dying Centurion default branch closes safely.
- [x] Run `py build\test_modernization_static.py`.
- [x] Run `py build\test_feature_audit_static.py`.
- [x] Run `py build\doctor.py --doctor-new-only`.
- [x] Run `cmd /c build_module.bat --no-cache`.

## Recently Fixed Old Bugs

- [x] Jester cheat "Thanks" route no longer leads into battle outside cheat mode.
- [x] `Ctrl+J` no longer triggers formation rank/disengage command.
- [x] Court lady honor duel no longer traps player in a Continue menu.
- [x] Camp entry is guarded against stale encounter parties and bad hero stacks.
- [x] Late-game invalid party `-1` spam in nearby strength calculation fixed.
- [x] Chancellor lord recruitment revalidates lord pool and territory.
- [x] IEF dying Centurion dialogue default death reply closes safely.
- [x] Gaius Marcus lore dialogue soft-locks fixed.
- [x] Relic map "Jawel" typo fixed to "Jewel."
- [x] Mercenary lord faction cleanup after defeated kingdom fixed.
- [x] Antarian javelinmen have enough ammo for multi-wave battles.
- [x] Formation reset clears stale scripted orders.

## Build Gate

Before marking a modernization slice complete:

- [x] Focused static test passes.
- [x] `py build\test_feature_audit_static.py` passes.
- [x] `py build\doctor.py --doctor-new-only` reports 0 warnings.
- [x] `cmd /c build_module.bat --no-cache` completes successfully.
- [ ] Manual QA rows remain unchecked unless tested in-game.
