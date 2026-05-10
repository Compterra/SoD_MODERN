# Formation Layer Checklist

Goal: build a Total War-inspired, M&B 1.011-compatible formation layer using the operations and architecture already available in this repo.

This is not a PBOD wholesale port. It is a native-compatible battlefield command and positioning layer built around infantry, archers, and cavalry. The core design is "soft formations": troops are assigned deliberate positions and periodically reformed, but they are allowed to dissolve naturally when combat contact makes strict formation control feel bad or technically unreliable.

## Design Targets

- [ ] Make battles feel more commanded, less like three loose mobs colliding.
- [ ] Keep compatibility with M&B 1.011 operations in `compile/headers/header_operations.py`.
- [ ] Use the existing SoD battle panel and formation scripts as the base.
- [ ] Support infantry, archers, and cavalry as the main controllable groups.
- [ ] Avoid Warband-only/PBOD-only assumptions such as 9 divisions, team slots, agent division reassignment, runtime pavises, crouching, and ammo-slot swapping.
- [ ] Preserve normal M&B combat once formations enter melee.
- [ ] Keep scripts readable and tunable with named constants.
- [ ] Prefer visible battlefield behavior over a large preference framework.

## Hard Engine Boundaries

- [ ] Do not rely on `team_set_slot`, `team_get_slot`, `team_slot_eq`, or `team_slot_ge`.
- [ ] Do not rely on `agent_get_division` or `agent_set_division`.
- [ ] Do not rely on runtime scene prop spawning for formation behavior.
- [ ] Do not rely on runtime agent item-slot manipulation.
- [ ] Do not rely on Warband/WSE camera or input operations.
- [ ] Do not implement more than the engine's practical class groups: infantry, archers, cavalry.
- [ ] Assume agents can ignore or drift away from scripted destinations once combat begins.
- [ ] Assume pathing will be imperfect around obstacles, cliffs, siege props, and dense agent clusters.

## Existing Local Foundation

- [ ] Review `src/scripts/ZE_encounters/cf_formation.py`.
- [ ] Review `src/scripts/ZE_encounters/cf_formation_stagger.py`.
- [ ] Review `src/scripts/ZE_encounters/cf_formation_wedge.py`.
- [ ] Review `src/scripts/ZE_encounters/choose_formation_leader.py`.
- [ ] Review `src/scripts/ZE_encounters/formation_end.py`.
- [ ] Review `src/scripts/ZE_encounters/team_give_order_from_order_panel.py`.
- [ ] Review `src/scripts/ZE_encounters/update_order_panel.py`.
- [ ] Review `src/scripts/ZE_encounters/update_order_panel_checked_classes.py`.
- [ ] Review `src/scripts/ZE_encounters/update_order_panel_statistics_and_map.py`.
- [ ] Review `src/presentations/0011_battle/battle.py`.
- [ ] Review `src/mission_templates/0010_lead_charge/lead_charge.py`.
- [ ] Confirm current formation triggers in `lead_charge` still match generated `compile/module_mission_templates.py`.
- [ ] Confirm scripts are included in script order and generated into `compile/module_scripts.py`.

## FormRanks Reference Mining

`References/FormRanks` is a Mount&Blade Module System 1.010.0 reference and is much more relevant than the Warband PBOD stack. It avoids Warband team slots by using hidden temporary parties as formation vectors, party slots as structured state, agent slots for per-soldier formation metadata, and 1.011-era presentation/input operations.

- [ ] Use `docs/reports/formranks_extraction.md` as the source map before implementation.
- [ ] Use `docs/reports/formranks_overhaul_plan.md` as the pre-implementation design contract.
- [ ] Treat `References/FormRanks` as the advanced native-compatible reference.
- [ ] Do not port it wholesale until the smaller local formation layer is stable.
- [ ] Mine its architecture before mining individual geometry scripts.
- [ ] Preserve our existing SoD battle panel unless replacing it clearly removes complexity.
- [ ] Verify every imported operation against `compile/headers/header_operations.py`.
- [ ] Keep any copied constants renamed into a SoD namespace.
- [ ] Strip debug messages before any production implementation.

Important compatible ideas:

- [ ] Hidden party vectors: `formation_vector` and `formation_temp_vector` are spawned around `p_main_party`, disabled, and then used as slot-backed data stores.
- [ ] Array selection masks: eight controllable arrays are tracked with bit flags instead of Warband divisions.
- [ ] Agent state bitmasks: each agent stores array number, in-formation state, and leader state in one formation slot.
- [ ] Formation state bitmasks: each array stores formation type, auto-rotation, charge/fall-back state, speed, density, tactical charge, and engaged state.
- [ ] Formation temp stats: per-team buckets split soldiers into high infantry, low infantry, archers, two cavalry groups, and two horse-archer groups.
- [ ] Reform stages: AI arrays step through formation deployment before tactical charge, instead of instantly issuing every behavior at once.
- [ ] Leader election: formation leaders are elected by troop level and replaced when down.
- [ ] Centroid anchors: formation reference positions can be based on the current array centroid instead of a single leader's exact position.
- [ ] Maintain tick: formation destinations are refreshed once per second, not every frame.
- [ ] Relax-on-contact behavior: engaged arrays get a very large position tolerance so melee can breathe.
- [ ] Tactical charge: array-level charge/fall-back/speed state can move a formation as a body before melee.
- [ ] Auto-rotation: arrays can periodically face the average enemy position.
- [ ] Density controls: stand closer/spread out is treated as formation density, not only native order spam.
- [ ] Tactical map flags: battle presentations can display array markers and receive map-click orders.
- [ ] Command cursor: holding a key projects a ground arrow using `agent_get_look_position`, `particle_system_burst`, and a stored order rotation.
- [ ] Key configuration: formation hotkeys can be persisted in party slots, though this may be more UI than we need.

Reference files to mine:

- [ ] `References/FormRanks/module_constants.py` around formation constants and bitmasks.
- [ ] `References/FormRanks/module_mission_templates.py` around `frk_mt_triggers` and `frk_mt_ai_triggers`.
- [ ] `References/FormRanks/module_scripts.py` around `script_formation_agent_init`.
- [ ] `References/FormRanks/module_scripts.py` around `script_formation_formulate_arrays`.
- [ ] `References/FormRanks/module_scripts.py` around `script_cf_apply_formation`.
- [ ] `References/FormRanks/module_scripts.py` around `script_maintain_formation`.
- [ ] `References/FormRanks/module_scripts.py` around `script_formation_ai_tactics`.
- [ ] `References/FormRanks/module_scripts.py` around `script_cf_formation_ai_deploy_array_generic`.
- [ ] `References/FormRanks/module_scripts.py` around `script_formation_tactical_charge_generic`.
- [ ] `References/FormRanks/module_scripts.py` around `script_formation_tactical_charge_cavalry`.
- [ ] `References/FormRanks/module_scripts.py` around `script_formation_tactical_charge_ranged`.
- [ ] `References/FormRanks/module_scripts.py` around `script_formation_line`, `script_formation_phalanx`, `script_formation_wedge`, and `script_formation_square`.
- [ ] `References/FormRanks/module_presentations.py` around `prsnt_battle_formations`.
- [ ] `References/FormRanks/module_presentations.py` around the formation key configuration presentation.

Features to adapt cautiously:

- [ ] Eight arrays are probably too much for first implementation; start with three class groups and keep the array model optional.
- [ ] High/low infantry split is interesting for elite guards and levy blocks, but should wait until infantry/archer/cavalry formations are solid.
- [ ] Horse-archer split is useful only if our troop tree and order UX can support it clearly.
- [ ] Tactical charge is promising, but should be tested after basic hold/move/reform behavior.
- [ ] Cut Warcry/roar behavior entirely; morale and cohesion should show through movement, obedience, routing, and recovery.
- [ ] The order panel is powerful, but our UI should stay smaller unless playtesting proves the extra controls are worth it.
- [ ] Key remapping is not necessary for the first pass.
- [ ] Debug-only formation messages should not be retained.
- [ ] The reference uses some dense bit-packing; copy the idea, not necessarily the exact masks.

Operations already present in active `compile` that make this reference feasible:

- [ ] `spawn_around_party`
- [ ] `disable_party`
- [ ] `party_get_slot`
- [ ] `party_set_slot`
- [ ] `agent_get_slot`
- [ ] `agent_set_slot`
- [ ] `agent_set_scripted_destination`
- [ ] `agent_clear_scripted_mode`
- [ ] `agent_set_speed_limit`
- [ ] `agent_get_ammo`
- [ ] `agent_play_sound`
- [ ] `team_get_order_position`
- [ ] `team_set_order_position`
- [ ] `get_scene_boundaries`
- [ ] `position_transform_position_to_parent`
- [ ] `position_transform_position_to_local`
- [ ] `position_is_behind_position`
- [ ] `position_copy_rotation`
- [ ] `store_sqrt`
- [ ] `store_pow`
- [ ] `store_tan`
- [ ] `start_presentation`
- [ ] `mouse_get_position`
- [ ] `create_image_button_overlay`
- [ ] `create_check_box_overlay`
- [ ] `overlay_set_alpha`
- [ ] `overlay_set_val`
- [ ] `overlay_set_mesh_rotation`
- [ ] `overlay_animate_to_alpha`
- [ ] `particle_system_burst`

Recommended adaptation path:

- [ ] Phase 1: keep current class-based groups and add FormRanks-style formation state wrappers.
- [ ] Phase 2: add centroid anchoring and leader replacement.
- [ ] Phase 3: add density and auto-rotation controls.
- [ ] Phase 4: add tactical map click-to-move for active formations.
- [ ] Phase 5: add simple AI opening deployments using archer line, infantry ranks/phalanx, and cavalry wedge.
- [ ] Phase 6: consider array splitting only after class-group formations feel good.
- [ ] Phase 7: connect array/class cohesion to the morale layer.

## Formation Constants

Create or centralize tunables in `src/constants/module_constants.py`.

- [ ] Add `sod_formation_none`.
- [ ] Add `sod_formation_line`.
- [ ] Add `sod_formation_ranks`.
- [ ] Add `sod_formation_shieldwall`.
- [ ] Add `sod_formation_loose`.
- [ ] Add `sod_formation_stagger`.
- [ ] Add `sod_formation_wedge`.
- [ ] Add `sod_formation_square`.
- [ ] Add `sod_formation_reserve`.
- [ ] Add infantry spacing constants.
- [ ] Add archer spacing constants.
- [ ] Add cavalry spacing constants.
- [ ] Add minimum group size constants for each formation.
- [ ] Add reform interval constants.
- [ ] Add melee-distance thresholds for stopping or reducing reform.
- [ ] Add fallback constants for low troop counts.
- [ ] Add max row width constants for infantry, archers, and cavalry.
- [ ] Add high-ground search radius constants if AI opening tactics use formations.

Suggested starting values:

- [ ] Infantry close spacing: 100 cm.
- [ ] Infantry normal spacing: 140 cm.
- [ ] Infantry loose spacing: 220 cm.
- [ ] Archer normal spacing: 250 cm.
- [ ] Archer stagger row offset: 125 cm.
- [ ] Cavalry normal spacing: 250-300 cm.
- [ ] Cavalry wedge row depth: 350 cm.
- [ ] Reform interval while holding: 3 seconds.
- [ ] Reform interval while moving: 2 seconds.
- [ ] Stop hard reform when nearest enemy is within 600-900 cm.

## State Model

Since team slots are not available, use globals and/or party slots carefully. `FormRanks` proves that hidden temporary parties can serve as mission-local formation vectors in M&B 1.010/1.011-style module systems.

- [ ] Decide whether formation mode is mission-only global state or persistent party state.
- [ ] Decide whether to use a small FormRanks-style hidden party vector for formation state.
- [ ] If using a hidden party vector, allocate it at mission start with `spawn_around_party`.
- [ ] If using a hidden party vector, disable it immediately with `disable_party`.
- [ ] If using a hidden party vector, clear all relevant slots before use.
- [ ] Add globals for player infantry formation mode.
- [ ] Add globals for player archer formation mode.
- [ ] Add globals for player cavalry formation mode.
- [ ] Add globals for ally infantry formation mode if allied formations are supported.
- [ ] Add globals for ally archer formation mode if allied formations are supported.
- [ ] Add globals for ally cavalry formation mode if allied formations are supported.
- [ ] Add globals for AI team formation mode only if needed.
- [ ] Add globals for last reform time per controlled class.
- [ ] Add globals for formation anchor positions only if positions cannot be reconstructed from current orders.
- [ ] Reset mission-only globals before or at mission start.
- [ ] Clear formation modes on battle end.
- [ ] Clear formation modes when the player charges all troops.
- [ ] Clear formation modes when a group count drops below minimum.

Possible global naming:

- [ ] `$sod_form_player_infantry_mode`
- [ ] `$sod_form_player_archers_mode`
- [ ] `$sod_form_player_cavalry_mode`
- [ ] `$sod_form_player_infantry_reform_time`
- [ ] `$sod_form_player_archers_reform_time`
- [ ] `$sod_form_player_cavalry_reform_time`
- [ ] `$sod_form_player_reform_enabled`

## Script Architecture

Prefer small scripts with clear inputs and outputs.

- [ ] Add `script_sod_formation_get_class_count`.
- [ ] Add `script_sod_formation_choose_leader`.
- [ ] Add `script_sod_formation_get_anchor_position`.
- [ ] Add `script_sod_formation_find_nearest_enemy_distance`.
- [ ] Add `script_sod_formation_should_reform`.
- [ ] Add `script_sod_formation_apply`.
- [ ] Add `script_sod_formation_apply_line`.
- [ ] Add `script_sod_formation_apply_ranks`.
- [ ] Add `script_sod_formation_apply_stagger`.
- [ ] Add `script_sod_formation_apply_wedge`.
- [ ] Add `script_sod_formation_apply_square`.
- [ ] Add `script_sod_formation_apply_reserve`.
- [ ] Add `script_sod_formation_end_class`.
- [ ] Add `script_sod_formation_end_all`.
- [ ] Add `script_sod_formation_store_mode_for_class`.
- [ ] Add `script_sod_formation_reform_tick`.
- [ ] Keep old scripts as compatibility wrappers until migrated.
- [ ] Avoid stuffing all modes into one giant script.

Recommended script inputs:

- [ ] `arg1`: team number.
- [ ] `arg2`: class group, one of `grc_infantry`, `grc_archers`, `grc_cavalry`.
- [ ] `arg3`: formation mode.
- [ ] `arg4`: anchor mode, such as leader/current order/player/map click.
- [ ] `arg5`: spacing override or zero for default.

Recommended script outputs:

- [ ] `reg0`: success/failure.
- [ ] `reg1`: agents placed.
- [ ] `reg2`: group count.
- [ ] `reg3`: nearest enemy distance if calculated.

## Agent Selection Rules

- [ ] Iterate with `try_for_agents`.
- [ ] Require `agent_is_alive`.
- [ ] Require `agent_is_human`.
- [ ] Require `agent_get_team` equals target team.
- [ ] Require `agent_get_class` equals target class.
- [ ] Exclude the player agent when issuing AI destinations if needed.
- [ ] Exclude horses and non-human agents.
- [ ] Avoid assigning destinations to agents already in immediate melee if nearest enemy is too close.
- [ ] Optional: skip routed/fleeing agents if current scripts expose reliable state.
- [ ] Optional: skip agents that are too far away from the main group to avoid weird cross-map pathing.

## Formation Leader Rules

- [ ] Prefer non-player team leader if that leader belongs to the target class.
- [ ] Otherwise choose a living human agent in the target class.
- [ ] Prefer highest-XP troop as class leader.
- [ ] Prefer non-ranged infantry for infantry/wedge leadership.
- [ ] Avoid choosing archers or throwers as wedge leaders if possible.
- [ ] For player-team formations, allow the player to be anchor for "follow me" modes.
- [ ] If no valid leader exists, fail gracefully and clear formation mode.
- [ ] Store chosen leader in a local variable only; do not require persistent agent IDs between ticks.

## Anchor Position Rules

Supported anchors:

- [ ] Current class leader position.
- [ ] Player agent position.
- [ ] Team order position from `team_get_order_position`.
- [ ] Tactical map click position from `prsnt_battle`.
- [ ] Pre-battle deployment offset from battle start.

Implementation checks:

- [ ] Copy anchor position into a working position register.
- [ ] Point the formation toward nearest enemy when possible.
- [ ] Fall back to facing the player or leader's current rotation if no enemy is found.
- [ ] Set destination positions to ground level where supported.
- [ ] Avoid moving anchor into invalid terrain if possible.
- [ ] Keep all formation calculations local to a predictable range of `pos` registers.

## Infantry Formations

### Infantry Line

- [ ] Arrange infantry in a broad line.
- [ ] Width scales with group count.
- [ ] Use normal spacing by default.
- [ ] Center the line on the anchor.
- [ ] Place leader near center/front.
- [ ] Support one-rank line for small groups.
- [ ] Support two-rank line for medium groups.
- [ ] Support three or more ranks for large groups.
- [ ] Keep row depth less than cavalry row depth.
- [ ] Rotate line to face enemy.

Acceptance:

- [ ] 10 infantry form a compact line.
- [ ] 25 infantry form a line with second rank.
- [ ] 60 infantry form a coherent block instead of a single absurdly wide line.

### Infantry Ranks

- [ ] Arrange infantry in deeper ranks.
- [ ] Use narrower max row width than line mode.
- [ ] Place stronger troops toward front only if feasible without inventory sorting.
- [ ] Keep rows aligned behind anchor.
- [ ] Use this as the default "hold center" formation.

Acceptance:

- [ ] Infantry can advance in a block-like mass before contact.
- [ ] Repeated reform does not cause constant sideways shuffling.

### Shieldwall-Flavored Formation

- [ ] Use close spacing.
- [ ] Prefer two to four ranks.
- [ ] Issue `mordr_stand_closer` before or after formation placement.
- [ ] Issue `mordr_hold` if defending.
- [ ] Do not require shield detection unless cheap and reliable.
- [ ] Treat this as a close-rank infantry formation, not a true shieldwall animation system.

Acceptance:

- [ ] Infantry visibly bunches into a denser front.
- [ ] Formation does not trap troops in endless micro-positioning after melee begins.

### Square / Defensive Mass

- [ ] Implement only after line/ranks are stable.
- [ ] Use a compact rectangle or rough square.
- [ ] Face outer rows is probably not possible cleanly; do not overpromise.
- [ ] Use for anti-cavalry flavor and defensive AI posture.

Acceptance:

- [ ] Cavalry-facing infantry can be ordered into a compact defensive mass.
- [ ] The shape remains understandable before contact.

## Archer Formations

### Archer Line

- [ ] Arrange archers in a wide, loose line.
- [ ] Use larger spacing than infantry.
- [ ] Limit depth to one or two rows when possible.
- [ ] Place archers behind infantry when pre-battle plan asks for it.
- [ ] Face nearest enemy.
- [ ] Issue `mordr_hold`.
- [ ] Preserve `mordr_fire_at_will` or `mordr_hold_fire` from current order state where feasible.

Acceptance:

- [ ] Archers do not pile into one dense clump.
- [ ] Archers have better sightlines than current behavior.

### Archer Stagger

- [ ] Use alternating row offsets.
- [ ] Keep second row offset half spacing.
- [ ] Avoid too many rows.
- [ ] Prefer this for mixed archer/crossbow bodies.

Acceptance:

- [ ] 20 archers form a recognizable staggered line.
- [ ] 50 archers remain readable and not absurdly wide.

### Archer Fall-Back

- [ ] Optional after core formation work.
- [ ] If enemy distance is below threshold, move archers back along opposite facing vector.
- [ ] Do not spam fallback every tick.
- [ ] Do not fallback into map edge if scene boundaries are available.
- [ ] Stop fallback if infantry is between archers and enemy.

Acceptance:

- [ ] Archers can back up once or twice instead of suiciding into melee.
- [ ] Fall-back does not cause endless retreat loops.

## Cavalry Formations

### Cavalry Reserve

- [ ] Gather cavalry behind or to one flank of infantry.
- [ ] Use wider spacing.
- [ ] Issue hold or follow order depending on command mode.
- [ ] Keep reserve mode before charge.
- [ ] Disable frequent reform after charge.

Acceptance:

- [ ] Cavalry waits as a group instead of immediately scattering.
- [ ] Player can release cavalry with charge.

### Cavalry Wedge

- [ ] Improve existing `cf_formation_wedge.py`.
- [ ] Use cavalry-appropriate spacing.
- [ ] Choose leader carefully.
- [ ] Build rows from point to rear.
- [ ] Stop reforming once charge begins or enemies are close.
- [ ] Optionally issue charge after the wedge is mostly assembled.

Acceptance:

- [ ] Cavalry gathers into a triangular shape before charge.
- [ ] Wedge does not keep pulling riders out of combat.

### Cavalry Flank Position

- [ ] Compute left or right flank offset from infantry anchor.
- [ ] Move cavalry to flank reserve.
- [ ] Face enemy center.
- [ ] Provide separate left/right commands only after reserve mode works.

Acceptance:

- [ ] Cavalry can be placed on a flank before battle lines meet.
- [ ] AI cavalry can delay charge from a flank position.

## Reform Logic

Core idea: formations are refreshed while they are useful and relaxed when they become harmful.

- [ ] Add mission trigger for formation reform tick.
- [ ] Tick no faster than every 1 second globally.
- [ ] Per-class reform intervals should be 2-4 seconds.
- [ ] Reform only if formation mode is active.
- [ ] Reform only if class has enough living agents.
- [ ] Reform only if group is holding, advancing, or preparing.
- [ ] Do not hard-reform if nearest enemy is inside melee threshold.
- [ ] Do not hard-reform after all troops are ordered to charge.
- [ ] Do not reform routed/fleeing agents if detectible.
- [ ] Reduce reform frequency as casualties rise or melee begins.
- [ ] Clear mode when class count drops below minimum.

Possible reform states:

- [ ] Active: regular reform pulses.
- [ ] Loose: slower reform pulses.
- [ ] Suspended: no reform during melee.
- [ ] Cleared: formation mode off.

Acceptance:

- [ ] Troops hold recognizable shape before contact.
- [ ] Troops do not moonwalk around while actively fighting.
- [ ] Performance remains acceptable at high battle size.

## Battle Panel Integration

Build on `src/presentations/0011_battle/battle.py`.

- [ ] Add formation mode buttons for selected class.
- [ ] Add Line button.
- [ ] Add Ranks button.
- [ ] Add Loose/Stagger button.
- [ ] Add Wedge button for cavalry.
- [ ] Add Reserve button for cavalry.
- [ ] Add End Formation button.
- [ ] Keep buttons compact and readable.
- [ ] Make unavailable buttons no-op or hidden depending on UI limits.
- [ ] Preserve existing class checkbox behavior.
- [ ] When map is clicked, set hold position and apply current formation mode if active.
- [ ] Update visible order text after formation command.
- [ ] Avoid requiring listbox/numberbox/container overlays since active compile headers do not expose them.

Acceptance:

- [ ] Player can select infantry and choose ranks.
- [ ] Player can select archers and choose loose/stagger.
- [ ] Player can select cavalry and choose wedge/reserve.
- [ ] Map click sends selected groups to a location and formation reforms there.

## Keyboard/Trigger Integration

Current mission template references formation hotkeys/triggers in `lead_charge`.

- [ ] Audit existing formation hotkeys.
- [ ] Decide whether to keep, remove, or repurpose old formation triggers.
- [ ] Avoid adding many new keys if the presentation can handle commands.
- [ ] Ensure no hotkey conflicts with existing game controls.
- [ ] Provide display messages for formation changes.

Message examples:

- [ ] "Infantry forming ranks."
- [ ] "Archers spreading out."
- [ ] "Cavalry forming wedge."
- [ ] "Cavalry held in reserve."
- [ ] "Formation dismissed."

## Pre-Battle Hook

This belongs partly to PBOD-lite, but it feeds the Formation Layer.

- [ ] Add pre-battle plan option only after live formations are stable.
- [ ] Store desired formation modes for infantry, archers, cavalry.
- [ ] On battle start, apply formation modes after agents spawn.
- [ ] Use simple offsets: infantry center, archers behind, cavalry flank/reserve.
- [ ] Keep this optional and easy to clear.

Acceptance:

- [ ] Player can start battle with infantry center, archers behind, cavalry reserve.
- [ ] No permanent party stack reorder is required.

## AI Formation Use

Add after player formation work is stable.

- [ ] AI infantry can use ranks/line when holding.
- [ ] AI archers can use line/stagger when holding high ground.
- [ ] AI cavalry can use reserve/wedge before charging.
- [ ] AI stops maintaining formations once melee begins.
- [ ] AI posture should use existing `battle_tactic_*` scripts.
- [ ] Avoid adding complex state until player-side behavior is proven.

AI posture ideas:

- [ ] Defensive: infantry ranks, archers behind/on hill, cavalry reserve.
- [ ] Balanced: infantry advance, archers line, cavalry flank wait.
- [ ] Aggressive: infantry line advance, cavalry early charge.
- [ ] Archer-heavy: archers wide, infantry screen.
- [ ] Cavalry-heavy: cavalry grouped, infantry follows.

Acceptance:

- [ ] AI army looks intentionally arranged at battle start.
- [ ] AI does not freeze because it is trying to preserve perfect geometry.

## Morale And Cohesion Integration

The formation layer should eventually depend on battlefield morale and cohesion, not only scripted destination pulses. This repo already has several morale-like systems that need a cleaner shared model before formations can feel truly disciplined.

Existing surfaces to audit:

- [ ] `src/scripts/ZC_parties/get_player_party_morale_values.py` for campaign party morale.
- [ ] `src/scripts/ZH_heroes/npc_morale.py` for companion morale and morality grievances.
- [ ] `src/scripts/ZH_heroes/reduce_companion_morale_for_clash.py` for companion cohesion loss.
- [ ] `src/scripts/ZZ_common_array_processing/flee_enemies.py` for enemy panic/flee checks.
- [ ] `src/scripts/ZZ_common_array_processing/rout_enemies.py` for stronger enemy rout behavior.
- [ ] `src/scripts/ZZ_common_array_processing/flee_allies.py` for ally flee behavior.
- [ ] `src/scripts/ZZ_common_array_processing/rout_allies.py` for ally rout behavior.
- [ ] `src/mission_templates/_preamble/00_imports.py` for `formations_rally`, `formations_update_morale`, `formations_update_route`, kill-count bravery, and commander-duel morale flags.
- [ ] Any `script_battle_cry`, `script_rally`, `script_coherence`, `script_healthbars`, and morale display scripts.
- [ ] Menus and events that call `script_change_player_party_morale`.
- [ ] Companion quest outcomes that mention morale, discipline, courage, retreat, or troop welfare.

Refactor goals:

- [ ] Separate campaign morale from battle morale.
- [ ] Separate individual companion morale from troop/cohort morale.
- [ ] Add a battle-local cohesion concept that formations can read.
- [ ] Make rout/flee behavior use the same battle morale inputs as formation collapse.
- [ ] Make rally improve battle morale/cohesion temporarily instead of acting as a disconnected effect.
- [ ] Make commander death, commander duel outcome, casualties, nearby routs, and player bravery feed battle morale.
- [ ] Make discipline/training/leadership affect how long formations hold before soft collapse.
- [ ] Make low morale reduce reform frequency or formation obedience.
- [ ] Make high morale improve formation recovery after movement or shock.
- [ ] Keep morale math transparent enough to tune.

Suggested model:

- [ ] Campaign morale: long-term party mood from food, pay, size, leadership, company accounts, companion cohesion.
- [ ] Battle morale: mission-local willingness to keep fighting.
- [ ] Formation cohesion: mission-local ability of a class group to keep shape.
- [ ] Discipline: resistance to formation drift and panic.
- [ ] Shock: short-term penalty from casualties, nearby routing, cavalry impact, commander fall, being flanked, or being outnumbered.
- [ ] Rally: short-term recovery from player command, companion presence, commander victory, or battle cry.

Possible battle-local globals:

- [ ] `$sod_battle_player_morale`
- [ ] `$sod_battle_enemy_morale`
- [ ] `$sod_battle_ally_morale`
- [ ] `$sod_battle_player_infantry_cohesion`
- [ ] `$sod_battle_player_archer_cohesion`
- [ ] `$sod_battle_player_cavalry_cohesion`
- [ ] `$sod_battle_enemy_infantry_cohesion`
- [ ] `$sod_battle_enemy_archer_cohesion`
- [ ] `$sod_battle_enemy_cavalry_cohesion`
- [ ] `$sod_battle_recent_player_shock`
- [ ] `$sod_battle_recent_enemy_shock`
- [ ] `$sod_battle_last_rally_time`

Possible scripts:

- [ ] `script_sod_battle_morale_init`
- [ ] `script_sod_battle_morale_tick`
- [ ] `script_sod_battle_morale_apply_casualty_shock`
- [ ] `script_sod_battle_morale_apply_commander_event`
- [ ] `script_sod_battle_morale_apply_rally`
- [ ] `script_sod_battle_morale_get_team_to_reg`
- [ ] `script_sod_battle_cohesion_get_class_to_reg`
- [ ] `script_sod_battle_cohesion_modify_class`
- [ ] `script_sod_battle_should_class_hold_formation`
- [ ] `script_sod_battle_should_agent_flee`
- [ ] `script_sod_battle_store_morale_report_to_sreg`

Formation interactions:

- [ ] If class cohesion is high, reform normally.
- [ ] If class cohesion is moderate, reform more slowly and use looser spacing.
- [ ] If class cohesion is low, suspend hard formation and allow fallback/hold/charge only.
- [ ] If class cohesion collapses, clear scripted destinations and let rout/flee logic take over.
- [ ] Shieldwall/ranks should require higher cohesion than loose line.
- [ ] Cavalry wedge should require higher cohesion than reserve.
- [ ] Archer stagger should be tolerant of lower cohesion.
- [ ] Successful rally should restore enough cohesion to resume loose formation, not necessarily tight ranks.

Battle morale inputs:

- [ ] Starting party morale.
- [ ] Leadership and tactics.
- [ ] Companion/commander presence.
- [ ] Troop level/quality.
- [ ] Recent casualties.
- [ ] Nearby ally routs.
- [ ] Nearby enemy routs.
- [ ] Player kills/bravery messages.
- [ ] Commander duel win/loss.
- [ ] Pay strain.
- [ ] Fatigue.
- [ ] Hunger/supply pressure if available.
- [ ] Formation state: tight formations resist shock but suffer more if broken.

Battle morale outputs:

- [ ] Flee chance.
- [ ] Rout chance.
- [ ] Formation reform eligibility.
- [ ] Formation reform interval.
- [ ] Rally effectiveness.
- [ ] Battle UI/report text.
- [ ] Companion post-battle comments.
- [ ] Possible campaign morale aftermath.

Refactor sequencing:

- [ ] First document current morale/rout scripts and globals.
- [ ] Add static tests around existing morale script names and trigger inclusion before refactoring.
- [ ] Introduce new battle morale wrapper scripts without changing behavior.
- [ ] Route existing `flee_*` and `rout_*` calculations through shared helper scripts.
- [ ] Route `formations_rally` through shared rally helper.
- [ ] Expose class cohesion to formation reform checks.
- [ ] Tune only after behavior is centralized.

Acceptance:

- [ ] Formations hold longer when morale/cohesion is high.
- [ ] Formations loosen or break when morale/cohesion falls.
- [ ] Rally can restore a wavering line without magically resetting all panic.
- [ ] Elite troops and disciplined parties break less often than peasants or strained forces.
- [ ] Existing companion morale and campaign morale still work.
- [ ] Rout/flee behavior remains readable and does not spam scripted destinations.

## Performance Budget

- [ ] Avoid nested `try_for_agents` loops inside frequent triggers where possible.
- [ ] Count agents and place agents in a single pass when possible.
- [ ] Do nearest-enemy checks less often than formation placement if expensive.
- [ ] Keep reform tick interval conservative.
- [ ] Avoid per-frame formation work.
- [ ] Test at small, medium, and high battle sizes.
- [ ] Watch for stutter during reform pulses.

Suggested limits:

- [ ] No formation script should run every frame.
- [ ] Global formation tick should be no faster than 1 second.
- [ ] Per-class reform should usually be 2-4 seconds.
- [ ] AI formation reform should be less frequent than player reform.

## Safety Rules

- [ ] Never force movement for dead or invalid agents.
- [ ] Never assume player agent exists.
- [ ] Check `main_hero_fallen` where appropriate.
- [ ] Check battle result before reforming.
- [ ] Fail gracefully when no agents exist for selected class.
- [ ] Avoid touching siege-specific behavior until field battles are stable.
- [ ] Do not apply field formations in town/village/tournament/tutorial missions unless explicitly intended.
- [ ] Keep formation triggers mostly scoped to `lead_charge` first.

## Static Tests

Add focused static tests under `build/`.

- [ ] Test formation constants exist.
- [ ] Test new scripts are included in generated scripts.
- [ ] Test `lead_charge` includes formation reform trigger.
- [ ] Test unsupported operations are not introduced.
- [ ] Test formation scripts use `agent_set_scripted_destination`.
- [ ] Test formation scripts do not use Warband-only team slots.
- [ ] Test presentation has formation command buttons if UI work is added.
- [ ] Test battle panel still routes native orders.
- [ ] Test no raw PBOD slot constants are copied.

Potential test file:

- [ ] `build/test_formation_layer_static.py`

Forbidden-op assertion list:

- [ ] `team_set_slot`
- [ ] `team_get_slot`
- [ ] `team_slot_eq`
- [ ] `team_slot_ge`
- [ ] `agent_get_division`
- [ ] `agent_set_division`
- [ ] `spawn_scene_prop`
- [ ] `agent_equip_item`
- [ ] `agent_unequip_item`
- [ ] `agent_get_item_slot`
- [ ] `create_listbox_overlay`
- [ ] `create_number_box_overlay`
- [ ] `set_container_overlay`

## Build Verification

- [ ] Run `py build/doctor.py`.
- [ ] Run `py build/build_all.py`.
- [ ] Check generated `compile/module_scripts.py`.
- [ ] Check generated `compile/module_mission_templates.py`.
- [ ] Check generated `compile/module_presentations.py` if UI changed.
- [ ] Review doctor warnings for unknown identifiers.
- [ ] Review generated text for accidental unsupported ops.

## Playtest Matrix

### Small Field Battle

- [ ] 10 infantry vs 10 infantry.
- [ ] Infantry line forms.
- [ ] Infantry ranks form.
- [ ] Formation dissolves acceptably in melee.
- [ ] End formation works.

### Mixed Player Party

- [ ] 20 infantry, 15 archers, 10 cavalry.
- [ ] Infantry ranks hold center.
- [ ] Archers line up behind infantry.
- [ ] Cavalry reserve waits.
- [ ] Cavalry wedge forms.
- [ ] Charge releases cavalry cleanly.

### Large Battle

- [ ] 60+ infantry.
- [ ] 40+ archers.
- [ ] 30+ cavalry.
- [ ] Reform tick does not stutter badly.
- [ ] Lines remain readable before contact.
- [ ] No agents are stuck permanently.

### Terrain Stress

- [ ] Hill battle.
- [ ] Forest battle.
- [ ] River/uneven terrain.
- [ ] Map edge.
- [ ] Formation placement remains sane enough.

### AI Use

- [ ] AI defensive army holds formation.
- [ ] AI aggressive army advances.
- [ ] AI archer-heavy army protects archers.
- [ ] AI cavalry-heavy army does not trickle-charge immediately unless intended.

### Failure Cases

- [ ] Player falls.
- [ ] Class group wiped out.
- [ ] No cavalry present but cavalry command clicked.
- [ ] No archers present but archer command clicked.
- [ ] Reinforcements arrive.
- [ ] Battle ends while reform timer is active.

## Implementation Phases

### Phase 0: Audit And Baseline

- [ ] Document current formation scripts.
- [ ] Confirm current formation hotkeys.
- [ ] Add static forbidden-op test.
- [ ] Record current generated script names and triggers.
- [ ] Build once before changing behavior.

### Phase 1: Formation Constants And Wrappers

- [ ] Add constants.
- [ ] Add wrapper scripts with no behavior change.
- [ ] Route old formation calls through new wrapper where safe.
- [ ] Build.
- [ ] Verify no behavior regression.

### Phase 2: Infantry And Archer Geometry

- [ ] Implement line formation.
- [ ] Implement ranks formation.
- [ ] Implement archer line.
- [ ] Implement archer stagger.
- [ ] Add simple display messages.
- [ ] Build and static test.
- [ ] Playtest small and mixed battles.

### Phase 3: Cavalry Geometry

- [ ] Improve wedge.
- [ ] Add reserve position.
- [ ] Add flank position if reserve is stable.
- [ ] Stop reform on charge/contact.
- [ ] Build and static test.
- [ ] Playtest cavalry-heavy battles.

### Phase 4: Reform Pulses

- [ ] Add reform state globals.
- [ ] Add reform tick trigger.
- [ ] Add enemy-distance suspension.
- [ ] Add class-count minimums.
- [ ] Build and static test.
- [ ] Playtest high battle sizes.

### Phase 5: Battle Panel UI

- [ ] Add compact formation buttons.
- [ ] Wire buttons to formation scripts.
- [ ] Update selected-class behavior.
- [ ] Update tactical map click behavior.
- [ ] Build and static test.
- [ ] Playtest all player command flows.

### Phase 6: AI Formations

- [ ] Add AI opening formation choice.
- [ ] Integrate with `battle_tactic_init_aux`.
- [ ] Integrate with `battle_tactic_apply_aux`.
- [ ] Keep AI reform slower than player reform.
- [ ] Build and static test.
- [ ] Playtest defensive/aggressive AI.

### Phase 7: Pre-Battle Formation Plan

- [ ] Add pre-battle plan storage.
- [ ] Add encounter menu entry.
- [ ] Apply plan after spawn.
- [ ] Clear plan safely.
- [ ] Build and static test.
- [ ] Playtest encounter starts.

## Done Definition

The Formation Layer is "done enough" when:

- [ ] Player can form infantry into line/ranks.
- [ ] Player can form archers into line/stagger.
- [ ] Player can form cavalry into wedge/reserve.
- [ ] Tactical map movement works with active formations.
- [ ] Formations reform before contact and relax during melee.
- [ ] AI uses at least one visible opening formation posture.
- [ ] No unsupported Warband/PBOD operations are introduced.
- [ ] Field battles build and run without script errors.
- [ ] Performance remains acceptable at high battle size.
- [ ] The system feels like commanded M&B, not a brittle RTS impersonation.

## Design Notes

- [ ] Total War is the inspiration, not the promise.
- [ ] Prioritize opening deployment and movement discipline.
- [ ] Let melee become Mount & Blade melee.
- [ ] Prefer fewer reliable formation modes over many fragile ones.
- [ ] Make every formation readable from the player's saddle.
- [ ] Keep the player in command without burying them in menus.
- [ ] Tune by playtest, not by geometry alone.
