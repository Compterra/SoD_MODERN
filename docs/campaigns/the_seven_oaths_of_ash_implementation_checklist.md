# The Seven Oaths of Ash Implementation Checklist

> Status: **implementation checklist** for the target-state campaign document.  
> Source design: [`the_seven_oaths_of_ash.md`](./the_seven_oaths_of_ash.md)

## Status Key

- [x] Complete
- [-] In progress / partially complete
- [ ] Not started
- [!] Blocked or needs design decision

## Implementation Principle

Do not implement the whole campaign in one pass.

Build `The Seven Oaths of Ash` as vertical slices that remain buildable and playable after every milestone:

1. campaign state foundation
2. Act I ultimatum and Ashwick audit
3. Act II recruitment board
4. first defender recruitment slice
5. Act II return and Act III pressure
6. Oath Council and sector commitment
7. scalable siege phases
8. aftermath, endings, and companion unlocks
9. full dialogue polish and QA

Menus and quest logs are support structure. Dialogue and mission scenes carry the roleplaying.

## Readiness Snapshot

> Implementation status: **complete and build-verified**. The remaining unchecked items are manual in-game playtest routes only.

- [x] Campaign design document exists.
- [x] Six-act campaign structure exists.
- [x] Dialogue-first rule exists.
- [x] Seven defender roster exists.
- [x] Sword-training baseline exists.
- [x] Host scaling design exists.
- [x] Companion unlock design exists.
- [x] Dialogue Craft Checklist exists in the source design.
- [x] Exact source files for first implementation slice are mapped.
- [x] Campaign quest IDs are implemented.
- [x] Campaign globals or quest slots are implemented.
- [x] First unique NPC troop anchors are implemented.
- [x] First dialogue slice is implemented.
- [x] First build verification passes.
- [ ] First in-game playtest pass is complete.

## Polish Readiness Notes

- [x] Implementation checklist separates code-complete items from manual playtest-only items.
- [x] Menus remain structural: travel, staging, confirmation, and outcome summary.
- [x] Dialogue remains the primary surface for persuasion, moral choice, companion trust, and refusal.
- [x] Defender voices have craft anchors: sightlines, timber, oath, doors, discipline, bounded force, and sanctuary.
- [x] Companion aftermath lines name specific choices or violated values instead of generic rewards.
- [x] Ending archive records compact flags so later content can branch without rereading every quest slot.
- [x] Wulfred's host is framed as organized logistics and pressure, not generic bandit scaling.
- [x] Static tests now guard implementation completeness, dialogue craft, aftermath flags, and build surfaces.
- [ ] Manual playtest pass remains the only non-static completion gate.

## Open Decisions Before Code

- [x] Decide whether this campaign lives under `src/quests/` as a new campaign fragment or attaches to an existing quest framework file.
- [x] Decide exact quest prefix: recommended `seven_ash`.
- [x] Decide whether Ashwick is a fixed existing village, a selected protected settlement, or a temporary campaign center.
- [x] Decide whether Wulfred's host is a world party before the siege or only a mission-spawned campaign force.
- [x] Decide whether the seven defenders are full hero troops immediately or dialogue-only anchors until Act V.
- [x] Decide whether surviving defenders can all become companions at once or whether normal party-size limits apply.
- [x] Decide first vertical slice defenders: recommended Garric and Oswin.
- [x] Decide minimum verification commands for every milestone.

Decision notes:

- The design supports Act II as an open-ended recruitment board.
- Act III should not begin until Act II is formally closed.
- The player does not need to recruit all seven, but every defender road must be terminal or abandoned before Act III.
- The seven can become companions only through unique personal unlock conditions.
- Wulfred's host should scale against player field strength and use waves/sectors rather than one simple field battle.
- Initial implementation lives in `src/quests/0013_seven_oaths_of_ash_quests.py`.
- The first source prefix is `seven_ash` for quest IDs and `sod_seven_ash` for constants/scripts.
- Ashwick is currently implemented as a campaign-defined Ashwick scenario using existing menu and mission assets, not as a permanent map center.
- Wulfred's host is currently mission-spawned through scalable siege phases, not a persistent world party.
- The seven defenders are full hero troop anchors immediately, with companion joining gated in aftermath.
- Surviving defenders can all be invited, but only after survival plus unique personal unlock conditions.
- First vertical slice defenders are Garric and Oswin.
- Current minimum verification commands are `py build\test_seven_oaths_static.py`, `py build\build_quests.py`, `py build\build_scripts.py`, `py build\build_constants.py`, and `py build\doctor.py --doctor-new-only`.

## Milestone 0: Preflight and Source Mapping

Goal: identify exact files and local patterns before writing content.

### Source Inventory

- [x] Locate current campaign quest fragments under `src/quests/`.
- [x] Locate quest order file.
- [x] Locate dialogue order file.
- [x] Locate menu order files.
- [x] Locate mission template order files.
- [x] Locate troop definition sources for unique NPCs.
- [x] Locate existing quest slot constants.
- [x] Locate existing companion join logic.
- [x] Locate existing party strength or party-size helper patterns.
- [x] Locate existing siege or village-defense mission templates.
- [x] Locate existing QA/static test patterns for campaigns.

### Preflight Output

- [x] Record exact files to edit in this checklist.
- [x] Confirm generated files that will change.
- [x] Confirm build command for docs-only, source-only, and full output validation.
- [x] Confirm no unrelated dirty worktree files will be touched.

### Source Mapping Notes

- [x] Quest source file: `src/quests/0013_seven_oaths_of_ash_quests.py`
- [x] Quest order file: `src/quests/_order_quests.txt`
- [x] Dialogue source file: `src/dialogs/ZC02_townsfolk_and_special_npcs/trp_seven_ash_*`
- [x] Dialogue order file: `src/dialogs/_order_dialogs.txt`
- [x] Menu source file: `src/menus/start_game/seven_ash_ultimatum.py`, `src/menus/start_game/seven_ash_village_audit.py`, `src/menus/start_game/seven_ash_recruitment_map.py`
- [x] Menu order file: `src/menus/_order_game_menus.txt`
- [x] Mission template source file: `src/mission_templates/0073_seven_ash_outer_fields/`, `0074_seven_ash_palisade/`, `0075_seven_ash_breach/`, `0076_seven_ash_inner_streets/`, `0077_seven_ash_churchyard/`
- [x] Mission template order file: folder-driven under `src/mission_templates/`
- [x] Troop source file: `compile/module_troops.py`
- [x] Constants source file: `src/constants/module_constants.py`
- [x] Scripts source folder: `src/scripts/ZG_quests/`
- [x] Test file: `build/test_seven_oaths_static.py`
- [x] Companion join pattern: aftermath dialogue files use `party_add_members` and `slot_quest_seven_ash_companion_joined_bitmask`.
- [x] Party strength pattern: `script_party_count_fit_for_battle` feeds `slot_quest_seven_ash_player_strength_ultimatum` and `slot_quest_seven_ash_player_strength_siege`.

## Milestone 1: Campaign State Foundation

Goal: create persistent campaign state without live gameplay pressure.

### Quest IDs

- [x] Add `qst_seven_ash_ultimatum`.
- [x] Add `qst_seven_ash_village_audit`.
- [x] Add `qst_seven_ash_garric_ashbow`.
- [x] Add `qst_seven_ash_oswin_ditchwright`.
- [x] Add `qst_seven_ash_sir_aldrik_vane`.
- [x] Add `qst_seven_ash_mirelle_voss`.
- [x] Add `qst_seven_ash_tomas_reed`.
- [x] Add `qst_seven_ash_beren_hardhand`.
- [x] Add `qst_seven_ash_sister_elianor`.
- [x] Add `qst_seven_ash_return_to_ashwick`.
- [x] Add `qst_seven_ash_pressure_interlude`.
- [x] Add `qst_seven_ash_oath_council`.
- [x] Add `qst_seven_ash_outer_fields`.
- [x] Add `qst_seven_ash_palisade`.
- [x] Add `qst_seven_ash_breach`.
- [x] Add `qst_seven_ash_inner_streets`.
- [x] Add `qst_seven_ash_churchyard_stand`.
- [x] Add `qst_seven_ash_aftermath`.

### Core State

- [x] Add `campaign_status`.
- [x] Add `active_stage`.
- [x] Add `active_recruit_id`.
- [x] Add `act2_recruitment_board_open`.
- [x] Add `act2_recruitment_resolved_count`.
- [x] Add `act2_recruitment_complete`.
- [x] Add `act3_pressure_started`.
- [x] Add `days_remaining`.
- [x] Add `wulfred_pressure`.
- [x] Add `settlement_strain`.
- [x] Add `player_field_strength_at_ultimatum`.
- [x] Add `player_field_strength_at_siege`.
- [x] Add `wulfred_host_strength`.
- [x] Add `wulfred_elite_core_strength`.

### Ashwick Readiness

- [x] Add `ashwick_morale`.
- [x] Add `ashwick_food`.
- [x] Add `ashwick_labor`.
- [x] Add `ashwick_fortification`.
- [x] Add `ashwick_militia_training`.
- [x] Add `ashwick_intelligence`.
- [x] Add `ashwick_civilian_safety`.
- [x] Add village faction trust values for elders, youth, farmers, and refugees.

### Defender Bitmasks

- [x] Add recruited bitmask.
- [x] Add survival bitmask.
- [x] Add companion unlock bitmask.
- [x] Add companion refusal bitmask.
- [x] Add defender bond flags.
- [x] Add defender conflict flags.
- [x] Use defender bit allocation: Garric `1`, Oswin `2`, Aldrik `4`, Mirelle `8`, Tomas `16`, Beren `32`, Elianor `64`.

### Foundation Tests

- [x] Campaign state initializes with safe defaults.
- [x] Bitmask helpers count recruited defenders correctly.
- [x] Old saves or missing fields repair to safe defaults.
- [x] Campaign can be inactive without triggering content.

## Milestone 2: Unique NPC And Troop Anchors

Goal: create stable anchors before dialogue references them.

### Core NPCs

- [x] Add `trp_seven_ash_wulfred_carr`.
- [x] Add `trp_seven_ash_rafe_carrick`.
- [x] Add `trp_seven_ash_mother_hilda`.
- [x] Add `trp_seven_ash_reeve_martin`.
- [x] Add `trp_seven_ash_piers_wainwright`.
- [x] Add `trp_seven_ash_nell_harrow`.

### Seven Defenders

- [x] Add `trp_seven_ash_garric_ashbow`.
- [x] Add `trp_seven_ash_oswin_ditchwright`.
- [x] Add `trp_seven_ash_sir_aldrik_vane`.
- [x] Add `trp_seven_ash_mirelle_voss`.
- [x] Add `trp_seven_ash_tomas_reed`.
- [x] Add `trp_seven_ash_beren_hardhand`.
- [x] Add `trp_seven_ash_sister_elianor`.

### Wulfred Lieutenants

- [x] Add `trp_seven_ash_halvorn_pike`.
- [x] Add `trp_seven_ash_maud_ledger`.
- [x] Add `trp_seven_ash_sibert_crow_eye`.

### Equipment Rules

- [x] Give every defender a two-handed sword sidearm.
- [x] Preserve role weapons: Garric bow, Oswin tools/shield, Aldrik knightly arms, Mirelle knife/sword, Tomas infantry gear, Beren axe/sword, Elianor plain defensive sword.
- [x] Ensure no recruited defender spawns unarmed except in explicit captivity, disguise, or medical aftermath scenes.

## Milestone 3: Act I Ultimatum And Ashwick Audit

Goal: establish the crisis through dialogue and concrete settlement inspection.

### Ultimatum

- [x] Add opening scene with Rafe's sack of teeth, buckles, and village tokens.
- [x] Add Mother Hilda hostage question.
- [x] Add Rafe's "surety" answer.
- [x] Route final posture through dialogue before menu confirmation.
- [x] Implement choices: prepare alone, find defenders, call lordly aid, bargain, evacuate, kill messengers.
- [x] Set method and pressure flags from spoken decisions.

### Village Audit

- [x] Add palisade inspection.
- [x] Add granary inspection.
- [x] Add churchyard inspection.
- [x] Add mill bridge inspection.
- [x] Add outer farms inspection.
- [x] Add cellar inspection.
- [x] Add witness dialogue for Mother Hilda, Reeve Martin, Piers, and Nell.
- [x] Let player choose one immediate priority after dialogue.
- [x] Store readiness baseline.

### Act I QA

- [x] Ultimatum cannot fire twice.
- [x] Quest log points to audit after ultimatum.
- [x] Dialogue carries moral posture.
- [x] Menu only confirms broad direction.
- [x] Kill-messengers path spikes pressure and remains recoverable.

## Milestone 4: Act II Recruitment Board

Goal: make recruitment open-ended without becoming a choice-book menu.

### Board State

- [x] Add `mnu_seven_ash_recruitment_map`.
- [x] Track defender statuses: unknown, available, in_progress, recruited, refused, alienated, lost, abandoned.
- [x] Display travel targets and status summaries.
- [x] Prevent board from resolving recruitment directly.
- [x] Board routes to scenes/dialogues for every meaningful branch.

### Completion Gate

- [x] Count terminal defender roads.
- [x] Set `act2_recruitment_complete` only when all seven roads are terminal or player formally ends recruitment.
- [x] Allow early return after at least three defender roads are resolved.
- [x] Mark unresolved roads as abandoned when player ends recruitment.
- [x] Prevent Act III from starting before Act II closes.

### Act II Pacing

- [x] Add light courier reports at day bands.
- [x] Add rumors of Wulfred scouts during travel.
- [x] Make slow recruitment methods harder at low time.
- [x] Trigger emergency return state if days reach zero during Act II.

## Milestone 5: First Defender Slice, Garric And Oswin

Goal: prove the recruitment pattern with one social/ranged defender and one practical/engineering defender.

### Garric

- [x] Add Split Hart tavern target.
- [x] Add Garric opening scene with insult and visible room awareness.
- [x] Add Eda Flint witness testimony.
- [x] Implement best, hard, legal-promise, blackmail, and refusal routes through dialogue.
- [x] Update trust/debt/pride/fear values.
- [x] Add return scene on Ashwick watch platform.
- [x] Add companion unlock condition for public truth, disciplined fire, and no wasted militia charges.

### Oswin

- [x] Add Harrowcut Quarry target.
- [x] Add bridge-collapse inspection.
- [x] Add worker questioning.
- [x] Implement vindication, debt payment, limited authority, forced service, and refusal routes through dialogue.
- [x] Update fieldwork modifiers and trust/debt/fear values.
- [x] Add return scene at Ashwick palisade.
- [x] Add companion unlock condition for respected engineering authority and accepted hard fieldwork sacrifice.

### First Defender QA

- [x] Both recruitments require world travel.
- [x] Both recruitments have a witness or evidence step.
- [x] Both recruitments can fail or be refused without breaking Act II.
- [x] Both return scenes change Ashwick readiness.
- [x] Dialogue passes the craft checklist.

## Milestone 6: Remaining Defender Roads

Goal: implement all seven defender campaigns to the same standard.

### Aldrik

- [x] Add chapel target.
- [x] Add Mara of the Bridge witness.
- [x] Add public oath, paid contract, legal restoration, coercion, and refusal routes.
- [x] Add objection to dishonor during later plans.
- [x] Add companion unlock for lawful terms, public oath, prisoner mercy, and civilian protection.

### Mirelle

- [x] Add Low Lantern tavern target.
- [x] Add Tib informant moral test.
- [x] Add evacuation authority, spy deal, legal leverage, exposure threat, and refusal routes.
- [x] Add spy-route support for pressure interludes.
- [x] Add companion unlock for trusted dirty work used to save lives.

### Tomas

- [x] Add veterans' almshouse target.
- [x] Add Old Jory and Matteo witness split.
- [x] Add limited discipline, harsh command, train-the-trainers, fear route, and refusal routes.
- [x] Add militia discipline support for siege.
- [x] Add companion unlock for discipline without cruelty.

### Beren

- [x] Add fighting pit or outlaw camp target.
- [x] Add Ansel Miller witness.
- [x] Add fair contest, lawful enemy, spoils route, unrestrained route, and refusal routes.
- [x] Add Halvorn/breach interaction.
- [x] Add companion unlock for violence with boundary and purpose.

### Elianor

- [x] Add Saint Ormond's refugee camp target.
- [x] Add camp inspection.
- [x] Add sanctuary, limited refugee admission, funded camp, forced labor, and refusal routes.
- [x] Add infirmary and civilian evacuation support.
- [x] Add companion unlock for sanctuary, wounded protection, and mercy.

## Milestone 7: Act II Return And Act III Pressure

Goal: make the player feel what changed while they were away.

### Return Scene

- [x] Add `qst_seven_ash_return_to_ashwick`.
- [x] Show recruited defenders arriving or missing.
- [x] Mother Hilda asks how many beds to prepare.
- [x] Reeve Martin asks how much time, coin, and grain remain.
- [x] Nell watches the road behind the player.
- [x] Villagers react to honorable, paid, coerced, and missing defenders.
- [x] Set `act3_pressure_started`.

### Pressure Interludes

- [x] Add Burned Cow.
- [x] Add Knife-Marked Door.
- [x] Add Grain Riot.
- [x] Add Wulfred's Offer.
- [x] Add First Funeral.
- [x] Ensure each interlude has at least two local perspectives.
- [x] Ensure recruited defenders reframe relevant interludes.
- [x] Ensure outcomes affect readiness, pressure, trust, or later siege conditions.

## Milestone 8: Oath Council And Sector Commitment

Goal: turn preparation into a visible strategic commitment.

### Oath Council

- [x] Add church map scene.
- [x] Let every recruited defender mark the map in their voice.
- [x] Make missing defenders felt.
- [x] Ask the seven required council questions.
- [x] Implement final defense plans: Hold Palisade, Defense in Depth, Counterstroke, Cut the Head, Empty Village.
- [x] Include defender objections and support.
- [x] Confirm final plan only after dialogue.

### Sector Commitment

- [x] Let player assign troops to outer fields, palisade, gate reserve, inner streets, churchyard, and evacuation escort.
- [x] Let player assign companions or defenders as sector leaders.
- [x] Read cavalry, archers, elite infantry, militia, and defender strengths by sector.
- [x] Under-allocation creates casualties, fires, or breaches.
- [x] Over-allocation protects one sector while exposing another.

## Milestone 9: Scalable Siege

Goal: make the final battle dangerous for a normal SoD player army.

### Host Scaling

- [x] Store player field strength at ultimatum.
- [x] Store player field strength at siege.
- [x] Compute Wulfred host size using design formula.
- [x] Clamp Wulfred host to readable range, recommended 180-420 fighters.
- [x] For 50-85 player troops, produce about 240-310 Wulfred fighters.
- [x] Explain scaling in-world through scouts, Maud's logistics, Rafe's pressure, and allied brigands.

### Siege Phases

- [x] Add Outer Fields phase.
- [x] Add Palisade and Ditch phase.
- [x] Add Gate and Breach phase.
- [x] Add Inner Streets phase.
- [x] Add Churchyard Stand phase.
- [x] Spawn host in waves/sectors instead of one field battle.
- [x] Let preparation reduce later-phase enemy arrivals.
- [x] Let poor scouting, high pressure, or weak sector commitment increase fresh attackers.

### Wulfred Outcomes

- [x] Wulfred can be killed.
- [x] Wulfred can be captured.
- [x] Wulfred can escape.
- [x] Wulfred can be bargained with.
- [x] Wulfred can win.

## Milestone 10: Aftermath, Endings, And Companion Offers

Goal: resolve people, not just rewards.

### Immediate Aftermath

- [x] Count civilian deaths.
- [x] Count burned homes.
- [x] Count surviving defenders.
- [x] Resolve Wulfred state.
- [x] Check promises kept.
- [x] Check prisoner treatment.
- [x] Check whether Ashwick remained village, fortress, or refugee camp.

### Defender Epilogues

- [x] Add Garric epilogue and companion offer/refusal.
- [x] Add Oswin epilogue and companion offer/refusal.
- [x] Add Aldrik epilogue and companion offer/refusal.
- [x] Add Mirelle epilogue and companion offer/refusal.
- [x] Add Tomas epilogue and companion offer/refusal.
- [x] Add Beren epilogue and companion offer/refusal.
- [x] Add Elianor epilogue and companion offer/refusal.
- [x] Let qualifying survivors join as companions.
- [x] Let qualifying survivors stay in Ashwick as trainers/contacts.
- [x] Let non-qualifying survivors refuse with personal reasons.
- [x] Memorialize dead defenders by craft and relationship.

### Endings

- [x] Implement Seven Oaths Kept.
- [x] Implement Ashwick Stands.
- [x] Implement Wall of Names.
- [x] Implement Empty Houses.
- [x] Implement Wulfred Broken.
- [x] Implement Wulfred Escaped.
- [x] Implement Bargain Brand.
- [x] Implement Blood for Ash.
- [x] Implement Long Road From Ashwick.
- [x] Implement Palisade Grave.
- [x] Implement New Wolf.
- [x] Implement Common Bell.

## Dialogue Implementation Gate

Every major scene must pass this gate before the milestone is marked complete.

### General

- [x] Scene has a clear dramatic job.
- [x] Scene starts from a visible situation.
- [x] Scene changes a state, relationship, clue, pressure value, or player understanding.
- [x] Important choices are spoken lines, not labels.
- [x] Quest log records the result after dialogue.
- [x] Menu does not replace moral or relationship-changing dialogue.

### Voice

- [x] Garric lines use sightlines, range, patience, cover, or wasted lives.
- [x] Oswin lines use wood, earth, measures, failure points, or preventable collapse.
- [x] Aldrik lines use oath, shame, witness, restraint, or public duty.
- [x] Mirelle lines use doors, lies, secrets, exits, or fear behavior.
- [x] Tomas lines distinguish discipline from cruelty.
- [x] Beren lines show force, insult, hunger, or violence being bounded.
- [x] Elianor lines name water, wounds, shelter, refugees, or mercy under pressure.
- [x] Villager lines use concrete local stakes.
- [x] Wulfred's host sounds practical and organized.

### Companion Offers

- [x] Each offer names a specific player decision.
- [x] Each refusal names a violated value or unfinished duty.
- [x] Staying in Ashwick feels honorable.
- [x] Joining the player explains why leaving Ashwick is acceptable.

## QA And Verification

### Static QA

- [x] Add or update campaign static tests.
- [x] Assert quest IDs exist.
- [x] Assert core globals/slots exist.
- [x] Assert defender bitmasks use the agreed allocation.
- [x] Assert all defender troop templates include sword sidearms.
- [x] Assert recruitment board cannot complete a defender without dialogue/scene state.
- [x] Assert Act III cannot begin before Act II is complete.
- [x] Assert companion unlocks require survival plus unique conditions.
- [x] Assert Wulfred host scaling clamps to configured range.
- [x] Assert 50-85 player troops produce non-trivial host strength.

### Manual QA

- [ ] Start campaign and answer ultimatum through every posture.
- [ ] Complete Ashwick audit and verify readiness values.
- [ ] Recruit Garric best route.
- [ ] Recruit Garric hard/blackmail route.
- [ ] Refuse Garric and verify Act II remains valid.
- [ ] Recruit Oswin best route.
- [ ] Recruit Oswin debt/forced route.
- [ ] Resolve three defender roads and end recruitment early.
- [ ] Resolve all seven defender roads.
- [ ] Trigger standard Act III return.
- [ ] Trigger late Act III return.
- [ ] Trigger emergency Act III return.
- [ ] Play each pressure interlude.
- [ ] Run Oath Council with all seven.
- [ ] Run Oath Council with missing defenders.
- [ ] Play siege with weak player party.
- [ ] Play siege with 50-85 player troops.
- [ ] Play siege with overwhelming player army.
- [ ] Verify each Wulfred outcome.
- [ ] Verify each defender companion offer path.
- [ ] Verify each defender refusal path.
- [x] Verify endings store compact flags.

### Build Commands

- [x] Run `py build\doctor.py --doctor-new-only`.
- [x] Run relevant campaign static tests.
- [x] Run dialogue immersion/static tests after dialogue changes.
- [x] Run full build if order files, dialogs, menus, scripts, mission templates, troops, or generated module output changed.

## Definition Of Done

The campaign implementation is complete only when all of these are true:

- [x] The campaign can be started, suspended, completed, failed, and archived safely.
- [x] Act II is open-ended and Act III is gated behind Act II closure.
- [x] Menus guide structure while dialogue carries roleplaying decisions.
- [x] All seven defender roads are implemented with witnesses/tests.
- [x] All seven defenders are sword-trained and combat-capable.
- [x] Wulfred scales to player strength and attacks through waves/sectors.
- [x] The final siege can resolve multiple ways.
- [x] Surviving defenders can become companions only through unique personal conditions.
- [x] Non-joining survivors have meaningful trainer/contact/farewell outcomes.
- [x] Dialogue passes the craft checklist.
- [x] Static tests and build verification pass.
- [ ] At least one full in-game playthrough validates the campaign from ultimatum to aftermath.
