# The Road to the Crown Implementation Checklist

> Status: **implementation checklist** for the target-state campaign document.  
> Source design: [`the_road_to_the_crown.md`](./the_road_to_the_crown.md)
>
> Startup note, 2026-05-09: RTC content remains in the module as parked reference/vertical-slice work. The live new-game handoff is restored to the original SoD `mnu_banner_selection` path until the intro is deliberately overhauled.

## Status Key

- [x] Complete
- [-] In progress / partially complete
- [ ] Not started
- [!] Blocked or needs design decision

## Implementation Principle

Do not implement the full campaign in one pass.

Build the campaign as vertical slices that leave the module buildable and playable after each milestone:

1. campaign state foundation
2. Act I opening slice
3. Act II first pressure test
4. quest-framework verification
5. companion reaction layer
6. Act III route seeding
7. Act IV branch locks
8. Act V imperial resolution
9. endings and successor unlocks

Each slice should prove one more part of the branch tree while preserving the same quest-framework lifecycle vocabulary:

- `advance_stage`
- `complete`
- `fail`
- `abort`
- campaign-level `split_to_branch`
- campaign-level `merge_back`
- campaign-level `overlay_and_return`
- campaign-level `suspend_and_replace`
- campaign-level `terminate_old_and_start_new`

## Readiness Snapshot

- [x] Campaign design document exists.
- [x] Campaign branch tree exists.
- [x] Chapter-to-quest mapping exists.
- [x] Act I first implementation slice is defined.
- [x] Core NPC roster is defined.
- [x] Core identity, reputation, pressure, and ending flags are named.
- [x] Exact code storage locations for campaign flags are chosen.
- [x] First NPC troop/dialogue entries are implemented.
- [x] First quest chain is authored.
- [x] First quest chain is build-verified.
- [x] First Act II-to-ending simulation memory thread is authored.
- [ ] First quest chain is play-verified.

## Open Decisions Before Live Gameplay Wiring

- [x] Decide where campaign state flags live: globals, quest slots, troop slots, or a mixed pattern.
- [x] Decide naming convention for campaign globals or slots.
- [x] Decide whether Act I uses temporary menu scenes, party encounters, or existing centers.
- [x] Decide first refugee camp location or placeholder center.
- [x] Decide whether custom NPCs are full hero troops immediately or dialogue-only placeholders first.
- [x] Decide whether Garran, Lysara, and Odran can join the party later or remain campaign NPCs.
- [x] Decide whether Imperial scout parties use existing troops or a new temporary troop template.
- [x] Decide how companion approval deltas are stored for the first slice.
- [x] Decide minimum build command for verification after each milestone.

Decision note:

- Act I currently uses temporary start-game menu scenes for the vertical slice; physical parties/centers can replace or augment them later.
- The first refugee camp is abstracted through `mnu_rtc_borrowed_names` and `mesh_pic_camp`; no world-center placement is required for this implementation slice.
- Custom NPCs are full unique troop anchors with dialogue entries, but they remain campaign NPCs rather than companions for now.
- The Imperial scout/courier interaction uses the unique `trp_rtc_imperial_courier` anchor rather than a full scout party template.
- Companion approval deltas are stored through the existing `script_sod_companion_apply_player_action` system.
- The minimum milestone verification command is `py build\doctor.py`, with targeted builders/tests used when source fragments change.

## Milestone 0: Preflight and Source Mapping

Goal: identify the exact source files and helper patterns to use before writing campaign content.

### Source Inventory

- [x] Locate current quest content fragments under `src/quests/`.
- [x] Locate `_order_quests.txt` and confirm how new quest fragments are registered.
- [x] Locate existing startup or story quest examples.
- [x] Locate dialogue files or generators used for quest conversations.
- [x] Locate troop definitions for unique NPCs or quest-giver-style agents.
- [x] Locate existing global variable or slot naming patterns.
- [x] Locate build verification scripts for quest lowering.
- [x] Locate existing companion approval or companion reaction hooks.

### Preflight Output

- [x] Add a brief source mapping note to this checklist or a separate implementation note.
- [x] Confirm first files to edit.
- [x] Confirm no unrelated dirty worktree changes will be touched.

### Source Mapping Note

- Quest content fragments live under `src/quests/`.
- New quest fragments are registered in `src/quests/_order_quests.txt`.
- The Road to the Crown first slice now lives in `src/quests/0011_road_to_crown_quests.py`.
- The quest builder lowers fragments into `compile/module_quests.py` through `build/build_quests.py`.
- Existing schema-backed patterns are in `src/quests/0001_prison_break_chain.py`, `src/quests/0009_story_and_meta_quests.py`, and `src/quests/0010_sample_campaign_quests.py`.
- Character creation already stores origin, faith, adult-life, and motive values through `$background_type`, `$background_answer_2`, `$background_answer_3`, `$background_answer_4`, `$g_sod_country`, and `$g_sod_faith`.
- Existing background constants live in `src/constants/module_constants.py`: `cb_antares`, `cb_marina`, `cb_aden`, `cb_villian`, `cb_zerrikan`, faith constants, `cb3_*`, and `cb4_*`.
- Quest runtime and chain state slots already exist in `src/constants/module_constants.py`, including `slot_quest_sod_runtime_*` and `slot_quest_sod_chain_*`.
- Quest chain scripts already exist under `src/scripts/ZG_quests/`, including `sod_quest_chain_set`, `sod_quest_chain_advance`, branch scripts, runtime complete/fail/abort scripts, and journal update scripts.
- Dialogue fragments are ordered by `src/dialogs/_order_dialogs.txt`; campaign-specific live dialogue can be added under the startup/special-NPC dialogue folders after NPC strategy is chosen.
- Companion reaction hooks are supported by existing companion campfire menus under `src/menus/camp/` and quest memory dialogue scripts under `src/scripts/ZG_quests/`.
- Unique RTC troop anchors are generated in `compile\ids\ID_troops.py`: `trp_rtc_garran_ashwake`, `trp_rtc_lysara_veyne`, `trp_rtc_imperial_courier`, `trp_rtc_tamsin_reedhand`, `trp_rtc_celeste_di_marina`, and `trp_rtc_brother_odran`.

### Initial Source Files Touched

- `src/quests/0011_road_to_crown_quests.py`
- `src/quests/_order_quests.txt`
- `compile/module_quests.py`
- `docs/campaigns/the_road_to_the_crown_implementation_checklist.md`
- `src/constants/module_constants.py`
- `src/scripts/ZG_quests/sod_rtc_initialize_campaign_state.py`
- `src/menus/0000_hardcoded_mb1011/choose_skill.py` for the live original-SoD handoff
- future intro-overhaul menu entry point, once designed

### Campaign State Decision

- Road to the Crown campaign state uses quest-owned slots on the campaign quest records.
- New slots are named `slot_quest_rtc_*` and live in `src/constants/module_constants.py`.
- Campaign identity values copy existing character creation globals instead of duplicating the background system.
- Starting identity source globals are `$background_type`, `$background_answer_2`, `$background_answer_3`, and `$background_answer_4`.
- Existing source globals `$g_sod_country` and `$g_sod_faith` remain the broader mod-level country/faith identity values.
- Campaign-specific enum constants are named `sod_rtc_*`.
- The first initializer is `script_sod_rtc_initialize_campaign_state`.
- The initializer is available for the future intro overhaul, but is not called from the live new-game handoff while RTC is parked.

### Definition of Done

- [x] Developer can name the exact files needed for Milestone 1.
- [x] Developer can run the current build or quest verification command.
- [x] No live gameplay wiring has been written before the storage and file targets are known.

## Milestone 1: Campaign State Foundation

Goal: create the minimum persistent state needed for the campaign to start and continue.

### Identity Flags

- [x] Add `origin_antares`.
- [x] Add `origin_marina`.
- [x] Add `origin_aden`.
- [x] Add `origin_villian`.
- [x] Add `origin_zerrikania`.
- [x] Add `faith_the_one`.
- [x] Add `faith_old_gods`.
- [x] Add `faith_void`.
- [x] Add `faith_enlightenment`.
- [x] Add `faith_natural_philosophy`.
- [x] Add `life_duelist`.
- [x] Add `life_intriguer`.
- [x] Add `life_philosopher`.
- [x] Add `life_trader`.
- [x] Add `motive_revenge`.
- [x] Add `motive_peace`.
- [x] Add `motive_bloodlust`.
- [x] Add `motive_riches`.

Implementation note:

- These identities use existing background constants: `cb_*`, `cb3_*`, and `cb4_*`.
- The RTC initializer stores them in `slot_quest_rtc_origin`, `slot_quest_rtc_faith`, `slot_quest_rtc_life`, and `slot_quest_rtc_motive`.

### Campaign Progress Flags

- [x] Add `campaign_road_to_the_crown` active marker.
- [x] Add act marker for `act_01_ashes`.
- [x] Add chapter marker support for `rtc_01_last_smoke`.
- [x] Add chapter marker support for `rtc_02_borrowed_names`.
- [x] Add chapter marker support for `rtc_03_hound_sign`.
- [x] Add generic route seed storage.
- [x] Add generic ending candidate storage.

### Early Reputation and Pressure Flags

- [x] Add `reputation_refugee`.
- [x] Add `reputation_foreign_noble`.
- [x] Add `reputation_free_captain`.
- [x] Add `reputation_trade_operator`.
- [x] Add `reputation_avenger`.
- [x] Add `reputation_unproven`.
- [x] Add `imperial_pressure_low`.
- [x] Add `act_01_choice_saved_wounded`.
- [x] Add `act_01_choice_saved_baggage`.
- [x] Add `act_01_choice_saved_papers`.
- [x] Add `companion_wary_mercy`.

Implementation note:

- Generic route storage uses `slot_quest_rtc_branch_seed`.
- Generic ending storage now uses `slot_quest_rtc_final_ending`, paired with `slot_quest_rtc_successor_unlock` for follow-up content queries.

### Integration Points

- [x] Connect character creation origin choices to campaign identity flags.
- [x] Connect faith selection to campaign identity flags.
- [x] Connect adult-life choice to campaign identity flags.
- [x] Connect motive choice to campaign identity flags.
- [x] Add debug or diagnostic output for identity flags if the project has a suitable pattern.

### Definition of Done

- [x] A new game can set all starting identity tags.
- [x] Campaign state can mark Act I as active.
- [x] Build succeeds.
- [x] No existing character creation behavior regresses.

Verification note:

- `py build\build_constants.py` completed with slot verification `warning=0 error=0`.
- `py build\build_scripts.py` completed successfully.
- `py build\build_game_menus.py` completed successfully.
- `py build\doctor.py` completed successfully with `OK: 0 warning(s)`.
- RTC startup is now parked from the live new-game handoff; static build and doctor checks pass for the parked content. Live new-game playthrough remains the separate play-verification item.

## Milestone 2: Act I Vertical Slice

Goal: implement the opening sequence and prove the campaign can progress through success and failure outcomes.

### `qst_rtc_last_smoke`

- [x] Author quest entry.
- [x] Add journal text.
- [x] Add objective: find survivors.
- [x] Add objective: choose what to save.
- [x] Add outcome: save wounded.
- [x] Add outcome: save baggage.
- [x] Add outcome: save military papers.
- [x] Add failure/compromise outcome: abandon road fight.
- [x] Add transition into `qst_rtc_borrowed_names`.

Implementation note:

- `script_sod_rtc_initialize_campaign_state` can start `qst_rtc_last_smoke`, but is not called from the live new-game handoff while RTC is parked.
- `script_sod_rtc_last_smoke_resolve` stores the salvage choice, writes an outcome note, completes or soft-fails the quest, and branches to `qst_rtc_borrowed_names`.
- `mnu_rtc_last_smoke` calls the outcome script when reached by a future intro flow.
- `compile\module_quests.py` contains `rtc_last_smoke_find_survivors`, `rtc_last_smoke_choose_salvage`, and `rtc_last_smoke_reach_camp`.

### `qst_rtc_borrowed_names`

- [x] Author quest entry.
- [x] Add Lysara dialogue prompt.
- [x] Add public identity choice: fallen noble.
- [x] Add public identity choice: free captain.
- [x] Add public identity choice: trader.
- [x] Add public identity choice: refugee.
- [x] Add public identity choice: avenger.
- [x] Set matching reputation flag from each choice.
- [x] Add transition into `qst_rtc_hound_sign`.

Implementation note:

- `script_sod_rtc_borrowed_names_choose_identity` stores the public reputation, writes an identity note, completes the quest, and branches to `qst_rtc_hound_sign`.
- `mnu_rtc_borrowed_names` calls the identity script when reached by a future intro flow.
- `compile\module_quests.py` contains `rtc_borrowed_names_stabilize_camp` and `rtc_borrowed_names_choose_identity`.
- Borrowed Names now reacts to the Last Smoke salvage choice in menu text and applies early noble, commoner, merchant, method, or Imperial-pressure bias from the chosen public identity.

### `qst_rtc_hound_sign`

- [x] Author quest entry.
- [x] Add objective: investigate Imperial proof.
- [x] Add evidence option: captured courier seal.
- [x] Add evidence option: burned Calradian route map.
- [x] Add evidence option: survivor testimony.
- [x] Add evidence option: Imperial ration tokens.
- [x] Add evidence option: coded pacification order.
- [x] Add success transition to Act I stop point.
- [x] Add weak-evidence failure transition that still continues the campaign.

Implementation note:

- `script_sod_rtc_hound_sign_resolve` stores `sod_rtc_pressure_low`, stores the method seed, completes on strong evidence, soft-fails on weak evidence, and branches to `qst_rtc_door_into_calradia`.
- `mnu_rtc_hound_sign` calls the evidence script when reached by a future intro flow.
- `compile\module_quests.py` contains `rtc_hound_sign_find_evidence` and `rtc_hound_sign_interpret_warning`.
- Hound Sign now records distinct investigative footprints for open challenge, stolen order, doctrine warning, supply tracing, and rumor-only flight.
- Hound Sign now reacts to Last Smoke salvage: wounded survivors, stores, papers, or abandoned-road absence change the evidence framing and notes.
- Door Into Calradia now displays the Hound Sign proof style and adds matching-contact notes when the first Calradian door fits the evidence method.
- Door Into Calradia now also displays Last Smoke salvage and rewards matching the first contact to wounded survivors, baggage, papers, or abandoned-road speed.

### Act I NPCs

- [x] Add or identify `npc_garran_ashwake`.
- [x] Add or identify `npc_lysara_veyne`.
- [x] Add or identify `npc_brother_odran`.
- [x] Add first Garran greeting.
- [x] Add first Lysara greeting.
- [x] Add first Odran greeting.
- [x] Add at least one Imperial scout or courier interaction.

Implementation note:

- Unique troop anchors now exist for `trp_rtc_garran_ashwake`, `trp_rtc_lysara_veyne`, `trp_rtc_brother_odran`, and `trp_rtc_imperial_courier`.
- Act I dialogue nodes now exist for Garran during `qst_rtc_last_smoke` or `qst_rtc_hound_sign`, Lysara during `qst_rtc_borrowed_names`, Odran during `qst_rtc_last_smoke` or `qst_rtc_borrowed_names`, and the Imperial Courier during `qst_rtc_hound_sign`.
- Each first interaction records a quest note in the relevant RTC quest.

### Act I Stop Points

- [x] Implement `stop_act_01_survived`.
- [x] Implement `stop_act_01_poor_start`.
- [x] Confirm both stop points can lead to Act II.

Implementation note:

- `sod_rtc_stop_act_01_survived` and `sod_rtc_stop_act_01_poor_start` are recorded in `slot_quest_rtc_branch_seed` when `qst_rtc_hound_sign` resolves.
- Both stop outcomes are copied to `qst_rtc_door_into_calradia` and `qst_rtc_price_of_bread`.
- `mnu_rtc_door_into_calradia` reads the stop outcome and shows different arrival text for a strong Act I stop versus a poor-start Act I stop.
- Last Smoke now frames the opening salvage choice through homeland or faith and records a founding-pressure note for how survivors will judge the first sacrifice.

### Definition of Done

- [x] Act I can complete through wounded, baggage, or papers outcome.
- [x] Act I can fail softly through weak evidence or abandoned road pressure.
- [x] Act I always leaves the campaign in a valid state.
- [x] Build succeeds.
- [ ] A manual playthrough can reach the Act I stop point.

Verification note:

- `py build\build_scripts.py` completed successfully after adding RTC outcome helper scripts.
- `py build\build_game_menus.py` completed successfully after adding RTC start-game menus.
- `py build\build_dialogs.py` completed successfully after adding Act I RTC NPC greetings.
- `py build\build_constants.py`, `py build\build_scripts.py`, and `py build\build_game_menus.py` completed successfully after adding Act I stop state.
- `py build\doctor.py` completed successfully with `OK: 0 warning(s)`.
- `py build\test_rtc_campaign_static.py` verifies all Act I salvage paths call their resolver and jump to `mnu_rtc_borrowed_names`.
- Live engine playthrough is still pending.

## Milestone 3: Act II First Pressure Test

Goal: implement the first social and moral pressure test using the state created in Act I.

### `qst_rtc_door_into_calradia`

- [x] Author quest entry.
- [x] Add Antares contact path.
- [x] Add Marina contact path.
- [x] Add Aden contact path.
- [x] Add Villian contact path.
- [x] Add Zerrikanian contact path.
- [x] Add at least one faith overlay line.
- [x] Add trust outcome for noble, merchant, or commoner access.

Implementation note:

- `mnu_rtc_door_into_calradia` now provides five first-contact routes: noble patron, guild contact, gate captain, village, and road scout.
- `mnu_rtc_door_into_calradia` reads `slot_quest_rtc_faith` and displays a faith/worldview overlay for The One, Old Gods, The Void, Enlightenment, or Natural Philosophy.
- `mnu_rtc_door_into_calradia` reads `slot_quest_rtc_origin` and displays homeland-specific contact framing for Antares, Marina, Aden, Villian, and Zerrikania.
- `script_sod_rtc_door_into_calradia_choose_contact` records the first social contact, sets noble/merchant/commoner trust or method seeds, completes `qst_rtc_door_into_calradia`, and branches to `qst_rtc_price_of_bread`.
- The five routes are mechanically implemented as social access types, with origin and faith overlays shaping the opening narrative.

### `qst_rtc_price_of_bread`

- [x] Author quest entry.
- [x] Add Tamsin Reedhand interaction.
- [x] Add Celeste or merchant-side interaction.
- [x] Add Odran mercy-side interaction.
- [x] Add resolution: pay fairly.
- [x] Add resolution: negotiate labor for grain.
- [x] Add resolution: expose hoarding.
- [x] Add resolution: requisition by force.
- [x] Add resolution: raid bandit stores.
- [x] Add failure state: hunger pressure remains.

Implementation note:

- Unique troop anchors now exist in `compile/module_troops.py` and generated `compile/ids/ID_troops.py`: `trp_rtc_tamsin_reedhand`, `trp_rtc_celeste_di_marina`, and `trp_rtc_brother_odran`.
- Dialogue nodes now exist for Tamsin, Celeste, and Odran while `qst_rtc_price_of_bread` is active. Each speaker gives a factional position and records a quest note.
- `mnu_rtc_price_of_bread` provides the first player-facing bread-crisis menu and returns to normal banner selection after resolution.
- The bread scene now reads Act I salvage, first Calradian contact, and public reputation to alter the opening narrative lines before the player chooses a resolution.
- `qst_rtc_price_of_bread` now binds to a real nearby village through `slot_quest_target_center`.
- Tamsin, Celeste, and Brother Odran are stored as the local, merchant, and mercy witness anchors through existing quest slots.
- Grain pressure is stored qualitatively in `slot_quest_target_amount` rather than exposed as exact player-facing numbers.
- The raid-bandit-stores route remains menu-compatible, but road-scout starts can now prepare and remember a temporary nearby `pt_bandits` cache party before cleanup.
- All bread resolutions apply small local relation/prosperity aftermath to the remembered village.
- Price of Bread now records additional consequence notes from Last Smoke salvage and first Calradian contact, so the same bread resolution is judged differently by wounded survivors, baggage ledgers, saved papers, villages, guilds, nobles, or scouts.

### Trust and Pressure Flags

- [x] Add or wire `commoner_trust_high`.
- [x] Add or wire `commoner_trust_low`.
- [x] Add or wire `merchant_trust_high`.
- [x] Add or wire `merchant_trust_low`.
- [x] Add or wire `noble_trust_high`.
- [x] Add or wire `noble_trust_low`.
- [x] Add or wire `village_fear`.

Implementation note:

- Trust flags are now mutually cleaned before setting a new high/low result for commoner, merchant, or noble trust.
- `noble_trust_low` is set when the player has a noble patron and resolves the bread crisis by force.

### Definition of Done

- [x] Act II reads at least one Act I state flag.
- [x] Different Act I outcomes alter at least one line or condition.
- [x] `qst_rtc_price_of_bread` can complete in at least three ways.
- [x] `qst_rtc_price_of_bread` can fail softly without breaking the campaign.
- [x] Build succeeds.
- [ ] Manual playthrough confirms Act I to Act II continuity.

Verification note:

- `py build\build_quests.py` regenerated `compile/module_quests.py` successfully with `qst_rtc_door_into_calradia`.
- `py build\build_constants.py` regenerated constants successfully. The remaining slot warning is unrelated to RTC: duplicate troop slot value 140 for `slot_troop_companion_core_value_proof` and `slot_troop_discussed_rebellion`.
- `py build\build_scripts.py` regenerated `compile/module_scripts.py` with the Door Into Calradia contact script and Hound Sign handoff.
- `py build\build_game_menus.py` reported cache up-to-date, and `compile/module_game_menus.py` already contains `mnu_rtc_door_into_calradia`.
- `py build\build_game_menus.py` regenerated `compile/module_game_menus.py` after adding reactive Price of Bread lines for salvage, contact, and reputation state.
- `py build\build_dialogs.py` regenerated `compile/module_dialogs.py` after adding Tamsin, Celeste, and Odran dialogue nodes.
- `py build\build_scripts.py` and `py build\build_game_menus.py` regenerated after adding the raid-bandit-stores resolution.
- `py build\doctor.py` completed successfully with `OK: 0 warning(s)`.

## Milestone 4: Quest Framework Verification

Goal: prove that the first campaign slice behaves correctly in the advanced quest framework.

### Lifecycle Checks

- [x] `qst_rtc_last_smoke` can `complete`.
- [x] `qst_rtc_last_smoke` can `fail` without terminating the campaign.
- [x] `qst_rtc_borrowed_names` can `complete`.
- [x] `qst_rtc_hound_sign` can `complete`.
- [x] `qst_rtc_hound_sign` can `fail` softly.
- [x] `qst_rtc_door_into_calradia` can `complete`.
- [x] `qst_rtc_price_of_bread` can `complete`.
- [x] `qst_rtc_price_of_bread` can `fail` softly.
- [x] Stage advancement is recorded in the quest journal where supported.

### State Checks

- [x] Identity flags persist after quest transitions.
- [x] Reputation flags persist after `qst_rtc_borrowed_names`.
- [x] `imperial_pressure_low` persists after `qst_rtc_hound_sign`.
- [x] Trust flags persist after `qst_rtc_price_of_bread`.
- [x] The Price of Bread target village and pressure memory persist through the implemented RTC spine.
- [x] Failure states do not overwrite unrelated success flags.

### Build and Diagnostics

- [x] Run quest build verification.
- [x] Run module build verification.
- [x] Check generated quest output if available.
- [x] Check quest journal output if available.
- [x] Record any warnings in this checklist.

Verification note:

- `py build\build_quests.py` regenerated `compile/module_quests.py` successfully.
- `py build\build_scripts.py` regenerated `compile/module_scripts.py` after trust flag cleanup.
- `py build\doctor.py` completed successfully with `OK: 0 warning(s)`.
- `compile/module_quests.py` contains the generated RTC quest chain entries and staged quest text for the first campaign slice.
- `script_sod_quest_chain_advance` writes chain progress to `slot_quest_sod_journal_chain_progress`, and `script_sod_quest_journal_describe_to_s2` displays stage, chain, and state for tracked quests.

### Definition of Done

- [x] First slice passes build verification.
- [ ] First slice passes one manual success-path playthrough.
- [ ] First slice passes one manual soft-failure playthrough.
- [ ] No invalid quest state is observed.

## Milestone 5: Companion Reaction Layer

Goal: add lightweight companion reactions to the implemented Act I and Act II choices.

### First Reaction Hooks

- [x] Add Ymira or Jeremus reaction to saving wounded.
- [x] Add Marnid or Katrin reaction to saving baggage.
- [x] Add Garran or Firentis reaction to saving military papers.
- [x] Add Deshavi or Bunduk reaction to food handling.
- [x] Add Lezalit reaction to requisition by force.
- [x] Add companion warning for abandoning the road fight.

### Companion State

- [x] Add or wire `steady`.
- [x] Add or wire `wary`.
- [x] Add or wire `troubled`.
- [x] Add or wire `near_breaking`.
- [x] Add or wire `broken`.
- [x] Add or wire `redeemed`.

### Definition of Done

- [x] At least three companions can react to first-slice choices.
- [x] Companion reactions are behavior-based, not only branch-based.
- [x] Reactions do not block quest progression unless explicitly intended.
- [x] Build succeeds.

Implementation note:

- Road to Crown now feeds first-slice decisions into the existing companion approval framework through behavior actions: mercy, food security, roadcraft, village abuse, hunger, discipline, and Imperial warning.
- `steady`, `wary`, `troubled`, and `near_breaking` are supported by `script_sod_companion_get_approval_band`.
- `broken` and `redeemed` are wired through companion warning state: companions who leave after a final warning are marked `sod_companion_warning_broken`, and companions who recover from final-warning approval back to stable trust are marked `sod_companion_warning_redeemed`.
- `py build\build_scripts.py` regenerated `compile/module_scripts.py` after adding companion reaction hooks.
- `py build\build_constants.py`, `py build\build_scripts.py`, and `py build\build_dialogs.py` regenerated after adding explicit broken/redeemed warning states.
- `py build\doctor.py` completed successfully with `OK: 0 warning(s)`.

## Milestone 6: Act III Route Seeding

Goal: convert early reputation and trust into route seeds.

### `qst_rtc_three_offers`

- [x] Add noble protection offer.
- [x] Add paid steel offer.
- [x] Add people's road offer.
- [x] Add hidden quiet ledger offer.
- [x] Gate offers using reputation, trust, life path, or faith where appropriate.
- [x] Set route seed for `branch_legitimacy`.
- [x] Set route seed for `branch_mercenary`.
- [x] Set route seed for `branch_conquest`.
- [x] Set route seed for `branch_coalition`.
- [x] Set modifier seed for `branch_reform`.
- [x] Set modifier seed for `branch_betrayal`.
- [x] Set hidden seed for `branch_hidden_regime_maker`.

Implementation note:

- `qst_rtc_three_offers`, `qst_rtc_companions_take_sides`, and `qst_rtc_first_recognition` are now authored in the RTC quest chain.
- `qst_rtc_price_of_bread` now branches forward to `qst_rtc_three_offers` on both success and soft failure.
- `script_sod_rtc_three_offers_choose_route` sets exactly one primary route seed on `slot_quest_rtc_branch_seed` and copies it to the next Act III quests.
- Primary route choices currently cover legitimacy, mercenary, conquest, coalition, and hidden regime-maker. Reform, betrayal, and hidden regime-maker are stored as coexistable route flags.
- `mnu_rtc_three_offers` now provides the player-facing route-selection surface and gates offers through reputation, trust, Imperial pressure, and method seed.
- `qst_rtc_price_of_bread` now jumps into `mnu_rtc_three_offers` before returning to banner selection, and its resolver propagates reputation, trust, pressure, method, salvage, contact, and flags into Act III state.
- `qst_rtc_price_of_bread` also propagates the remembered bread village and qualitative grain pressure into `qst_rtc_three_offers`.
- `qst_rtc_three_offers` now prepares a temporary route-proof party target when an offer is chosen and carries it into the companion campfire before cleanup.
- `py build\build_scripts.py` and `py build\build_game_menus.py` regenerated after adding the route-selection menu.

### `qst_rtc_companions_take_sides`

- [x] Add camp dialogue after route seed.
- [x] Add at least one approval reaction.
- [x] Add at least one warning reaction.
- [x] Add at least one near-fracture condition.

Implementation note:

- `mnu_rtc_companions_take_sides` now gives a campfire reaction scene after Three Offers and before the campaign returns to normal start flow.
- `script_sod_rtc_companions_take_sides_resolve` applies route-specific companion reactions through the existing companion approval framework.
- The resolver records approval/warning flavor in quest notes and stores `slot_quest_rtc_companion_pressure` when any companion falls below wary/steady trust into near-fracture territory.
- `qst_rtc_companions_take_sides` now branches forward to `qst_rtc_first_recognition`.
- `qst_rtc_companions_take_sides` reacts to the remembered bread-village outcome in campfire text and companion approval pressure.
- The campfire is now interactive: the player can reassure, rebuke, compromise, or ignore the company's dissent, each with a different companion-action footprint.

### `qst_rtc_first_recognition`

- [x] Add recognition path for lawful claimant.
- [x] Add recognition path for free captain.
- [x] Add recognition path for trade power.
- [x] Add recognition path for people's defender.
- [x] Add recognition path for dangerous warlord.
- [x] Add recognition path for shadow operator.

Implementation note:

- `mnu_rtc_first_recognition` now presents first-recognition outcomes after the companion side-taking scene.
- `script_sod_rtc_first_recognition_resolve` records lawful claimant, free captain, trade power, people's defender, dangerous warlord, and shadow operator outcomes as named recognition constants.
- First Recognition raises Imperial pressure to `sod_rtc_pressure_rising`, stores the selected recognition label, and preserves or adjusts the route seed for the later Crown Council.
- First Recognition carries the remembered bread village and pressure into Crown Council as a public reputation concern.
- First Recognition now prepares a temporary recognition-witness party target and carries it into Crown Council before cleanup.
- Three Offers now includes bread-oath, books-oath, and witness-oath variants that choose existing route families while adding distinct commoner, merchant, or noble witness memory for later council play.
- Three Offers now reacts to Last Smoke salvage and first Calradian contact in both menu text and route notes, so early wounded, baggage, papers, village, guild, or scout context bends the public offer.
- Companions Take Sides now reacts directly to bread-oath, books-oath, and witness-oath choices, preserving the chosen offer into First Recognition and Crown Council.
- First Recognition now surfaces and records bread-oath, books-oath, and witness-oath variants, strengthening the matching commoner, merchant, or noble witness memory before Crown Council.
- `py build\build_constants.py`, `py build\build_scripts.py`, and `py build\build_game_menus.py` regenerated successfully after adding recognition state.

### Definition of Done

- [x] Act III can set one and only one primary route seed by default.
- [x] Modifier flags can coexist with primary route seed.
- [x] Companion state can worsen without crashing campaign flow.
- [x] Build succeeds.

## Milestone 7: Act IV Crown Branch Locks

Goal: turn route seeds into major campaign branches.

### `qst_rtc_crown_council`

- [x] Require or simulate noble witness.
- [x] Require or simulate commoner witness.
- [x] Require or simulate company witness.
- [x] Require or simulate faith, scholar, merchant, or military witness.
- [x] Add Maeron Vald challenge.
- [x] Add Septima Varro offer.
- [x] Add Vaska leverage option.
- [x] Add route lock for `branch_legitimacy`.
- [x] Add route lock for `branch_mercenary`.
- [x] Add route lock for `branch_conquest`.
- [x] Add route lock for `branch_coalition`.
- [x] Add route lock for `branch_restoration`.
- [x] Add route lock for `branch_imperial`.
- [x] Add hidden override for `branch_hidden_regime_maker`.
- [x] Add failure outcome for `branch_failure_fractured_claim`.

Implementation note:

- `qst_rtc_crown_council` is now authored with witness-gathering and challenge-answer stages.
- `mnu_rtc_crown_council` now follows First Recognition and presents Maeron's challenge, Septima's Imperial offer, Vaska's gated leverage option, restoration, seeded-route lock, and fractured-claim failure.
- `script_sod_rtc_crown_council_resolve` simulates noble, commoner, company, and fourth witness categories from existing trust, recognition, and companion-pressure state.
- The resolver sets `sod_rtc_flag_route_locked` for successful council locks and fails into `sod_rtc_branch_fractured_claim` if the witness set is incomplete or the player chooses failure.
- The resolver can treat the remembered bread village as a commoner witness concern; good bread outcomes strengthen testimony, while force or unresolved hunger can give Maeron a vulnerability to press.
- Crown Council now lets the player put the bread witness forward or open merchant books as evidence tactics, allowing Price of Bread outcomes to actively answer Maeron instead of only passively coloring the council.
- Crown Council now visibly and mechanically consumes bread-oath, books-oath, and witness-oath memory, reinforcing the matching commoner, merchant, or noble witness set before Maeron's validation.
- Hidden regime-maker remains gated behind the previous quiet-ledger route and is presented as Vaska's leverage, not as an always-visible generic branch button.

### Definition of Done

- [x] Crown Council can lock a route.
- [x] Crown Council can fail into fractured claim state.
- [x] Hidden regime maker gate is checked but not exposed directly as a simple menu choice.
- [x] Act V receives the locked branch state.
- [x] Build succeeds.

## Milestone 8: Act V Imperial Resolution

Goal: resolve the selected crown branch under Imperial pressure.

### `qst_rtc_hounds_terms`

- [x] Add Marius or Septima terms by branch.
- [x] Add reject terms path.
- [x] Add negotiate delay path.
- [x] Add accept terms path.
- [x] Add talks collapse failure.

Implementation note:

- `qst_rtc_hounds_terms` is now authored as the Act V receiver for the locked Crown Council branch.
- `mnu_rtc_hounds_terms` presents route-specific Marius or Septima terms for legitimacy, mercenary, conquest, coalition, restoration, imperial, hidden regime-maker, and fractured-claim routes.
- `script_sod_rtc_crown_council_resolve` now copies the locked branch and supporting state into `qst_rtc_hounds_terms` and branches forward on council success.
- `script_sod_rtc_hounds_terms_resolve` supports rejecting terms, negotiating delay, accepting terms, and talks collapse.
- Accepting terms bends the branch toward `branch_imperial`; talks collapse fails into fractured-claim pressure with `sod_rtc_pressure_invasion`.
- Hound's Terms now lets the Empire weaponize, minimize, or reframe the remembered bread-village outcome.
- Hound's Terms now prepares a temporary Imperial envoy party target near the player and cleans it up after the terms resolve.
- Hound's Terms now lets the player release, detain, counter-demand through, or mishandle the envoy; that diplomatic posture carries into War of Witnesses flavor.
- Hound's Terms now attacks bread-oath, books-oath, and witness-oath identities directly, records the Imperial pressure note, and carries that oath memory into War of Witnesses separately from envoy handling.

### `qst_rtc_war_of_witnesses`

- [x] Add witness protection target.
- [x] Add sacrifice witness path.
- [x] Add route-specific target variants.
- [x] Add side-crisis handoff to `campaign_the_last_banner_of_the_east`.

Implementation note:

- `qst_rtc_war_of_witnesses` is now authored as the second Act V quest.
- `mnu_rtc_war_of_witnesses` frames the witness target by locked route: court witnesses, payroll road, Imperial vanguard, coalition allies, homeland survivors, Imperial loyalty sacrifice, ledger witnesses, or fractured-claim remnants.
- `script_sod_rtc_hounds_terms_resolve` now carries non-collapse Hound's Terms outcomes into `qst_rtc_war_of_witnesses`.
- `script_sod_rtc_war_of_witnesses_resolve` supports direct witness protection, witness sacrifice, route-specific target variants, and a Last Banner of the East side-crisis handoff note.
- War of Witnesses now treats the remembered bread village as a concrete threatened witness and applies small local relation consequences when that witness is protected or sacrificed.
- War of Witnesses now prepares a temporary route-colored threat party target and cleans it up after the current menu-compatible resolution.
- War of Witnesses now records how the Hound's Terms envoy was handled and carries that diplomatic posture into Last Road.
- War of Witnesses now unlocks an envoy-leverage response when the Hound's Terms envoy was detained or answered with a counter-demand, letting diplomacy/rhetoric blunt the witness hunt.
- War of Witnesses now targets bread-oath, books-oath, and witness-oath identities differently, adjusting commoner, merchant, or noble trust depending on whether the oath survives or is wounded.

### `qst_rtc_last_road`

- [x] Add hold the line strategy.
- [x] Add strike the Hound strategy.
- [x] Add starve the Empire strategy.
- [x] Add break the seal strategy.
- [x] Add accept the collar strategy.
- [x] Add catastrophic loss failure.

Implementation note:

- `qst_rtc_last_road` is now authored as the final-strategy Act V quest.
- `mnu_rtc_last_road` presents route-aware strategy framing and supports hold the line, strike the Hound, starve the Empire, break the Imperial seal, accept the collar, and catastrophic loss.
- `script_sod_rtc_war_of_witnesses_resolve` now carries successful witness-war outcomes into `qst_rtc_last_road`.
- `script_sod_rtc_last_road_resolve` records the chosen final strategy, applies companion reactions, and fails into fractured-claim pressure on catastrophic loss.
- Last Road now uses the remembered bread village to color the final strategy and applies a small local consequence for holding the line or suffering catastrophic loss.
- Last Road now prepares a temporary strategy target party and cleans it up after the current menu-compatible resolution.
- Last Road now carries the Hound's Terms envoy posture into Final Confrontation for later ending flavor.
- Last Road now shows the Hound's Terms envoy posture before the final strategy choice, making diplomacy and rumor visible during campaign planning.
- Last Road now records a quest note and companion reaction from the Hound's Terms envoy posture, so the memory affects campaign planning before the ending.
- Last Road now unlocks a `turn the accusation back` strategy when the envoy dispute or envoy-leverage witness answer gives the player a rhetorical battlefield.
- Last Road now carries bread-oath, books-oath, and witness-oath identity into final strategy text and consequences, then forwards the oath memory into Final Confrontation.

### `qst_rtc_final_confrontation`

- [x] Add Marius defeated path.
- [x] Add Marius forced back path.
- [x] Add Marius overlord path.
- [x] Add player rejects personal rule path.
- [x] Add claim collapse path.

Implementation note:

- `qst_rtc_final_confrontation` is now authored as the Act V closing quest.
- `mnu_rtc_final_confrontation` reads the Last Road strategy and presents Marius defeated, Marius forced back, Marius overlord, unworn crown, and claim collapse outcomes.
- `script_sod_rtc_last_road_resolve` now carries successful Last Road strategies into `qst_rtc_final_confrontation`.
- `script_sod_rtc_final_confrontation_resolve` records the final outcome, applies companion reactions, succeeds non-collapse endings, and fails claim collapse.
- Final Confrontation now closes the remembered bread-village thread with outcome-specific flavor and local relation consequences.
- Final Confrontation now prepares a temporary route-ending target party and cleans it up after archiving the outcome.
- Final Confrontation now records ending flavor from the Hound's Terms envoy posture, so clean diplomacy, leverage, counter-demand, or muddled terms survive into the archive.
- Final Confrontation now shows the Hound's Terms envoy posture before the ending choice, making late diplomacy visible instead of only archived afterward.
- Final Confrontation now applies small companion and local-trust consequences from the envoy posture instead of treating it as text-only memory.
- Final Confrontation now gives the `turn the accusation back` Last Road strategy its own ending note and small witness/local-trust payoff.
- The campaign archive now stores `sod_rtc_flag_envoy_accusation_turned` when the ending was shaped by turning the envoy dispute back on Marius, allowing future successor arcs to recognize a public-accusation victory.
- Final Confrontation and the campaign archive now close bread-oath, books-oath, and witness-oath memory with ending notes and successor-arc founding pressure.

### Definition of Done

- [x] Every Act IV branch has at least one Act V resolution.
- [x] Act V can complete into a non-collapse ending.
- [x] Act V can fail into Crown of Ashes.
- [x] Imperial accommodation can complete into Crown of the Empire.
- [x] Build succeeds.

## Milestone 9: Endings and Successor Unlocks

Goal: archive the campaign result and unlock appropriate follow-up content.

### Ending Flags

- [x] Add `ending_crown_of_law`.
- [x] Add `ending_crown_of_iron`.
- [x] Add `ending_crown_of_coin`.
- [x] Add `ending_crown_of_ashes`.
- [x] Add `ending_crown_of_faith`.
- [x] Add `ending_crown_of_vengeance`.
- [x] Add `ending_crown_of_return`.
- [x] Add `ending_crown_of_empire`.
- [x] Add `ending_unworn_crown`.

### Successor Hooks

- [x] Unlock governance campaigns from Crown of Law.
- [x] Unlock rebellion or military reform from Crown of Iron.
- [x] Unlock merchant league content from Crown of Coin.
- [x] Unlock exile or redemption arc from Crown of Ashes.
- [x] Unlock schism or reform content from Crown of Faith.
- [x] Unlock survivor reckoning from Crown of Vengeance.
- [x] Unlock homeland restoration from Crown of Return.
- [x] Unlock province or imperial civil war content from Crown of the Empire.
- [x] Unlock league or protector arc from Unworn Crown.

### Definition of Done

- [x] Campaign archives exactly one primary ending.
- [x] Ending can be queried by later content.
- [x] Successor unlocks do not activate unrelated campaigns.
- [x] Build succeeds.

### Implementation Notes

- Added query slots `slot_quest_rtc_final_ending` and `slot_quest_rtc_successor_unlock` on `qst_rtc_final_confrontation`.
- Added `sod_rtc_ending_*` and `sod_rtc_successor_*` constants for all documented endings and follow-up arcs.
- Added `script_sod_rtc_archive_campaign_ending`, called by `script_sod_rtc_final_confrontation_resolve` after final outcome resolution.
- The archive script records one primary ending and one successor hook only; later campaigns can inspect those slots without auto-starting unrelated content.
- Verified with `py build\doctor.py`: 0 warnings.

## Polish and QA Pass

Goal: make the implemented campaign slice feel intentional, readable, and maintainable.

### Text Polish

- [x] Journal text has consistent tense and tone.
- [x] NPC dialogue matches origin and faith tone rules.
- [x] Player choices clearly communicate consequences.
- [x] Failure text is not confusing or punitive when the campaign continues.
- [x] No placeholder or debug text appears in player-facing strings.

Verification note:

- Polished RTC menu choices for Price of Bread, Crown Council, Hound's Terms, War of Witnesses, Last Road, and Final Confrontation so major choices state their consequence in player-facing terms.
- Replaced implementation-facing ending archive notes with in-world ending notes that still signal the follow-up arc.
- Updated the final quest description and campaign metadata now that the implemented slice reaches endings.
- Scanned RTC player-facing menu, quest, script note, and dialogue text for placeholder/debug wording; remaining matches are checklist planning items, not player-facing strings.

### Technical QA

- [x] Quest IDs match the design document.
- [x] Flag names match the design document.
- [x] No duplicate quest IDs.
- [x] No duplicate dialogue heads.
- [x] No unreachable required stage.
- [x] No terminal failure accidentally blocks later play.
- [x] Build diagnostics are clean or documented.
- [x] Price of Bread simulation continuity is guarded by quest diagnostics.

Verification note:

- `py build\doctor.py` completed successfully with `OK: 0 warning(s)` after adding ending archive slots, constants, and scripts.
- Generated constants contain `slot_quest_rtc_final_ending`, `slot_quest_rtc_successor_unlock`, and `sod_rtc_ending_*`.
- Generated scripts contain `script_sod_rtc_archive_campaign_ending`, and `script_sod_rtc_final_confrontation_resolve` calls it after recording the final outcome.
- Generated quests and menus contain the RTC chain from `rtc_last_smoke` through `rtc_final_confrontation`.
- `compile\ids\ID_quests.py` contains exactly one generated quest ID each for `qst_rtc_last_smoke` through `qst_rtc_final_confrontation`.
- `compile\ids\ID_menus.py` contains the matching menu sequence `menu_rtc_last_smoke` through `menu_rtc_final_confrontation`.
- The live new-game handoff currently parks RTC and routes to `mnu_banner_selection` for original SoD startup stability.
- RTC dialogue heads in `compile\module_dialogs.py` were grouped by `speaker::state`; no duplicate RTC dialogue heads were found.
- Terminal failures currently return to `mnu_banner_selection` after recording failed/ash/fractured state, so later play is not blocked by a missing next menu.
- Quest diagnostics now include a Road to Crown bread-continuity contract covering the target village, witnesses, qualitative pressure, local aftermath, companion/council/Imperial echoes, witness-war handling, and final outcome closure.

### Playtest Matrix

- [x] Act I wounded path.
- [x] Act I baggage path.
- [x] Act I papers path.
- [x] Act I abandoned road path.
- [x] Borrowed Names noble identity.
- [x] Borrowed Names captain identity.
- [x] Borrowed Names trader identity.
- [x] Borrowed Names refugee identity.
- [x] Borrowed Names avenger identity.
- [x] Price of Bread fair-pay path.
- [x] Price of Bread negotiation path.
- [x] Price of Bread force path.
- [x] Price of Bread failure path.

Verification note:

- Added `build\test_rtc_campaign_static.py` to prove the listed matrix routes are wired through menus, resolver scripts, and forward handoffs.
- `py build\test_rtc_campaign_static.py` completed successfully with `test_rtc_campaign_static: OK`.
- This is static route verification, not a live Warband click-through; the next true QA step is an in-engine smoke playthrough of at least one complete route.

## Current Recommended Next Step

Run a live in-engine smoke playthrough for the first campaign chain.

The implemented campaign spine now reaches Act V endings and archives a queryable result. Static route verification is complete; the only remaining checklist gaps are live/manual play-verification items such as reaching the Act I stop point, confirming Act I to Act II continuity, and checking one success and one soft-failure path in Warband.
