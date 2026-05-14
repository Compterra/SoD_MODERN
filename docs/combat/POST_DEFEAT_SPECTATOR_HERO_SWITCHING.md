# Post-Defeat Spectator / Hero Switching

Source reference: `References/108-WB/Source`

Date: 2026-05-13

## Purpose

The 108-WB post-defeat system lets the battle continue after the player falls. Instead of ending immediately, the player can watch surviving heroes, cycle camera focus, and in some cases take over a surviving allied hero.

For this project, the useful idea is not "mind reading" or direct feature copy. The useful idea is company continuity: if the captain is knocked down, the company can still fight under lieutenants, companions, or designated officers.

## Current Project Baseline

This project already has Jinnai's free-camera kit in:

- `src/mission_templates/_preamble/00_imports.py`

The current shared triggers are:

- `camera_trigger_1`: initializes `$camera_mode`.
- `camera_trigger_2`: toggles free camera after `main_hero_fallen` when the jump key is clicked.
- `camera_trigger_3` / `camera_trigger_4`: move the camera forward/backward.
- `camera_trigger_5` / `camera_trigger_6`: rotate left/right.
- `camera_trigger_7` / `camera_trigger_8`: raise/lower camera height.

Those triggers are already included in major mission templates such as `lead_charge`, village attacks, raids, sieges, and custom battles. So the project has post-death viewing, but not the 108-WB hero-follow and hero-takeover layer.

## 108-WB Source Anchors

Main mission-template implementation:

- `References/108-WB/Source/module_mission_templates.py`, around the repeated post-defeat camera blocks near line 5680.
- The same logic is duplicated through many battle and siege templates.

Hero selection presentation:

- `References/108-WB/Source/module_presentations.py`, `prsnt_choose_fighter_in_battle`, around line 13912.

Related globals:

- `$cam_move_style`
- `$cam_follow_target_no`
- `$cam_follow_agent`
- `$player_choose_control_hero`
- `$player_choose_control_agent`
- `$tutorial_message_show`
- `$pop_camera_on`

## 108-WB Behavior

### Defeat Initialization

When `main_hero_fallen` becomes true and `$cam_move_style` is still zero, 108-WB:

1. Enumerates alive human hero agents.
2. Assigns each eligible agent a temporary index in agent slot `43`.
3. Chooses a first `$cam_follow_agent`.
4. Falls back to a random alive human agent if the selected hero is invalid.
5. Sets `$cam_move_style` to active spectator mode.
6. Gives the player's team a fallback order so the army keeps acting.

### Spectator Guidance

While spectator mode is active, it repeatedly shows a tutorial message:

- Tab quits the battle.
- Space changes watching mode.
- Left/right mouse cycles heroes.
- WASD rotates camera.
- Direction keys move camera.
- Enter chooses a hero.
- Ctrl hides the message.

The text has typos in the reference source and should not be reused directly.

### Camera Cycling

Left/right mouse rebuilds the list of alive human hero agents, assigns temporary indexes, then moves `$cam_follow_target_no` backward or forward with wraparound.

The focused agent is validated by:

- Agent exists.
- Agent is alive.
- Agent is human.
- Troop is a hero.
- Troop is not in an excluded enemy-captain range.

If the current focus becomes invalid, the system searches for another alive human agent.

### Camera Modes

Space cycles `$cam_move_style` through follow modes. The exact engine opcodes are decompiled, but the observed pattern is:

- One mode is free/spectator movement.
- One mode follows a selected agent.
- One mode anchors behind or near the selected agent using `agent_get_look_position`, `agent_get_position`, and `mission_cam_set_position`.

This is stronger than our current free camera because it gives the player a meaningful subject to watch.

### Hero Takeover

Pressing Enter attempts to take control of the focused agent. 108-WB gates this through its own fantasy item/cooldown system, but structurally the takeover does this:

1. Requires `main_hero_fallen`.
2. Requires `$cam_follow_agent` to be valid and alive.
3. Requires the focused agent to belong to `p_main_party`.
4. Stores the followed troop as `$player_choose_control_hero`.
5. Stores the followed agent as `$player_choose_control_agent`.
6. Stores the old agent hit points.
7. Temporarily removes the chosen hero's horse in some mission types.
8. Removes or hides the old followed agent.
9. Calls `set_player_troop` on the chosen hero.
10. Spawns a new player-controlled agent at the old agent position.
11. Assigns the new agent to the player's team.
12. Restores horse equipment if it was temporarily removed.
13. Copies agent slots from the old hero agent to the new player agent.
14. Restores hit points.
15. Records a battle statistic for controlling another hero.
16. Resets camera state back to normal play.

That is powerful, but risky. It is also the part most likely to break missions if ported too casually.

### Custom Commander-Style Pre-Battle Acting Commander

Custom Commander has a safer pattern than 108-WB's mid-mission body swap: the player chooses an acting commander before battle. This Custom Commander-style pre-battle acting commander flow starts the mission with that hero as the player troop, then a trigger can spawn the real `trp_player` as an allied AI agent near the commander. This avoids removing or hiding an already-spawned hero agent, avoids broad agent slot copying, and makes multi-stage sieges much easier to reason about.

Implemented local flow:

1. Menus expose `Choose acting commander ({s7}).` before normal battle-entry options.
2. `mnu_sod_battle_commander_select` lists the player and fit companion heroes in the main party.
3. Battle-entry options call `script_cf_sod_battle_commander_can_start` instead of hard-locking on `trp_player` health.
4. Launch actions call `script_sod_battle_commander_apply_before_mission`, which sets the acting commander with `set_player_troop`.
5. Shared mission triggers call `script_sod_battle_commander_spawn_player_ally` to spawn the real player beside the acting commander when appropriate.
6. Siege, village raid, and inner-battle templates use the dismounted spawn variant so the real player does not appear mounted on walls or in tight scenes.
7. `mnu_battle_debrief` restores the real player's AI-agent health once, using the same first-aid-adjusted pattern as Custom Commander.
8. A map-free simple trigger resets the acting commander back to `trp_player`.

This is not the same as post-defeat hero takeover. It is a robust "let someone else lead this fight" flow, and it is a better first implementation because it has clean menu entry, mission entry, debrief, and reset boundaries.

## Risk Areas In The 108-WB Version

### Heavy Duplication

The post-defeat logic is pasted into many mission templates. That makes bug fixes expensive and creates a high chance of inconsistent behavior between battle types.

Improvement:

- Keep the system in one shared trigger bundle.
- Put repeated checks into scripts such as `script_sod_post_defeat_find_next_agent` and `script_sod_post_defeat_can_take_control`.

### Loose Agent Validity

108-WB often checks whether the agent exists and is alive, but fallback paths can still assign a random alive human agent, including agents that may not be appropriate for player focus.

Improvement:

- Separate "watchable" from "controllable."
- Watchable can include allied heroes, commanders, and optionally important enemies.
- Controllable should be much stricter: alive allied hero, in player party, not already routed, not prisoner, not scripted-only, not disallowed by mission.

### Global State Leakage

Globals like `$cam_follow_agent`, `$cam_move_style`, and `$player_choose_control_hero` must be reset cleanly or they can leak across missions.

Improvement:

- Initialize all post-defeat globals at `ti_before_mission_start`.
- Clear them on mission end.
- Use one `$sod_post_defeat_state` enum instead of multiple loosely related flags.

Suggested state enum:

- `0`: inactive.
- `1`: player fallen, spectator initialized.
- `2`: free camera.
- `3`: follow camera.
- `4`: takeover pending.
- `5`: takeover complete.
- `6`: disabled for this mission.

### Unclear User Input

108-WB uses several controls at once: jump, mouse left/right, space, enter, ctrl, movement keys. It is functional but noisy.

Improvement:

- Keep controls minimal.
- Suggested controls:
  - Jump: toggle free camera.
  - Left/right mouse or bracket keys: cycle focus.
  - Use/action key: take command if allowed.
  - Tab: retreat/resolve battle.
- Show one compact tutorial message only once, then rely on short status messages.

### Takeover Respawn Hazards

The 108-WB takeover uses `set_player_troop` and `spawn_agent`, then copies slots from the old agent. This can break if:

- The old agent is mounted.
- The scene has tight geometry.
- The agent is in a scripted duel, siege ladder, prison break, or cutscene.
- The player troop is not restored after the mission.
- Mission scripts expect the original player agent only.

Improvement:

- Phase in takeover after spectator mode is stable.
- Require explicit mission opt-in.
- Store and restore the original player troop.
- Spawn beside the old agent using a validated nearby position.
- Kill/hide/remove the old AI agent only after the new player agent is confirmed.
- Copy only known safe slots, not a broad numeric range.

### Team And Order Side Effects

108-WB issues team orders after player fall. That can accidentally override player battle plans or formation logic.

Improvement:

- On player fall, do not blindly issue team-wide orders.
- Instead:
  - If a second-in-command exists, transfer command context to that agent.
  - If no officer exists, apply morale shock or delayed rout checks.
  - Preserve current formation/order state unless the mission explicitly wants panic.

## Recommended Robust Design For This Project

### Phase 1: Robust Spectator Follow

Keep the current free camera and add agent focus.

Core behavior:

- On player fall, build a watch list of surviving allied heroes and captains.
- If none exist, fall back to any surviving allied agent.
- Let the player cycle focus.
- Camera follows the focused agent while allowing free-camera toggle.
- If the focused agent dies, automatically move to the next valid focus.

No takeover yet.

### Phase 2: Company Command Continuity

Add a designated second-in-command concept.

Eligibility examples:

- Companion has officer role.
- Companion loyalty is high enough.
- Companion is conscious and not routing.
- Companion is in the battle.
- Mission allows post-defeat command.

Effects:

- If eligible officer survives, battle continues with lower morale penalty.
- If no officer survives, player fall causes stronger morale shock.
- Post-battle report can say who held command.

This gives the feature economy and narrative meaning even before direct control transfer.

### Phase 3: Limited Hero Takeover

Allow direct control only in suitable battles.

Suggested gates:

- Global option enabled.
- Mission template opts in.
- Player has a valid second-in-command or companion.
- Focused agent is alive, allied, human, hero, and in `p_main_party`.
- No active duel, presentation lock, scripted scene, or conversation overlay.
- Cooldown or once-per-battle limit.

Suggested costs:

- Company morale hit when the captain falls.
- Extra morale recovery if the replacement officer wins.
- Companion may gain "took command" prestige.
- Companion may resent being used recklessly if wounded after takeover.

### Phase 4: Post-Battle Memory

Tie the system into battle ranking and honors.

Track:

- Captain fell.
- Who took command.
- Whether the company won afterward.
- Casualties after transfer.
- Officer wounded or survived.

This can generate world-event style aftermath:

- "Bunduk held the line after you fell."
- "Lezalit restored order, but the men whisper that command nearly broke."
- "No officer rose after you fell; the rout became inevitable."

## Suggested Scripts

These should be shared helpers, not pasted into each mission:

- `script_sod_post_defeat_init`
- `script_sod_post_defeat_clear`
- `script_sod_post_defeat_agent_is_watchable`
- `script_sod_post_defeat_agent_is_controllable`
- `script_sod_post_defeat_rebuild_watch_list`
- `script_sod_post_defeat_select_next_agent`
- `script_sod_post_defeat_focus_camera`
- `script_sod_post_defeat_try_take_control`
- `script_sod_post_defeat_restore_player_troop`
- `script_sod_post_defeat_record_aftermath`

## Suggested Globals / Slots

Globals:

- `$sod_post_defeat_state`
- `$sod_post_defeat_enabled`
- `$sod_post_defeat_mission_allows_takeover`
- `$sod_post_defeat_focus_agent`
- `$sod_post_defeat_focus_index`
- `$sod_post_defeat_focus_count`
- `$sod_post_defeat_original_player_troop`
- `$sod_post_defeat_control_troop`
- `$sod_post_defeat_control_agent`
- `$sod_post_defeat_takeover_used`
- `$sod_post_defeat_second_in_command`

Temporary agent slots:

- `slot_agent_sod_post_defeat_focus_index`
- `slot_agent_sod_post_defeat_old_agent`

Troop/company memory slots:

- `slot_troop_sod_times_took_command`
- `slot_troop_sod_post_fall_victories`
- `slot_troop_sod_post_fall_failures`
- `slot_troop_sod_last_took_command_hours`

## Mission Integration Pattern

Do not add the full logic to every mission template.

Recommended pattern:

1. Add shared triggers in `_preamble/00_imports.py`.
2. Keep existing `camera_trigger_1` through `camera_trigger_8` working.
3. Add a second shared bundle, for example `sod_post_defeat_spectator_triggers`.
4. Include the bundle only in battle-like missions that can safely continue after player fall.
5. Set `$sod_post_defeat_mission_allows_takeover` during `ti_before_mission_start` for missions that allow control transfer.

Suggested first mission targets:

- `lead_charge`
- siege wall attacks
- village raids
- village attack bandits
- custom battle

Suggested exclusions:

- prison breaks
- tutorials
- town/village center scenes
- duel missions
- scripted companion trials
- any mission that must end on player fall

## Edge Cases To Handle

- No allied agents survive.
- No allied heroes survive, but regular troops survive.
- Focused agent dies while camera follows them.
- Focused agent routs, is knocked unconscious, or leaves the mission.
- Player falls while a presentation is already active.
- Battle ends while spectator tutorial is active.
- Reinforcements spawn after player fall.
- The selected hero is mounted.
- The selected hero is using scene-specific equipment.
- Original player troop must be restored after mission.
- Inventory chest/scene props should not be moved unless the mission specifically requires it.
- The battle result should not be forced to defeat merely because the player fell.
- Formation/order scripts should continue without being spammed by fallback orders.

## Best Implementation Stance

The robust version should treat this as three separate systems:

1. Post-defeat camera.
2. Command continuity.
3. Optional hero takeover.

They should be built and tested separately. Camera follow can be broadly enabled. Command continuity can be tied to companion/company systems. Hero takeover should remain opt-in because it touches player troop identity, agent spawning, mission result logic, and post-battle recovery.

## Mission Classification Snapshot

Current shared-camera templates:

- `0005_bandits_at_night/bandits_at_night.py`
- `0010_lead_charge/lead_charge.py`
- `0011_village_attack_bandits/village_attack_bandits.py`
- `0012_village_raid/village_raid.py`
- `0013_besiege_inner_battle_castle/besiege_inner_battle_castle.py`
- `0014_besiege_inner_battle_town_center/besiege_inner_battle_town_center.py`
- `0015_castle_attack_walls_defenders_sally/castle_attack_walls_defenders_sally.py`
- `0016_castle_attack_walls_belfry/castle_attack_walls_belfry.py`
- `0017_castle_attack_walls_ladder/castle_attack_walls_ladder.py`
- `0050_custom_battle/custom_battle.py`

Safe spectator and command-continuity templates:

- `lead_charge`
- `village_attack_bandits`
- `village_raid`
- `besiege_inner_battle_castle`
- `besiege_inner_battle_town_center`
- `castle_attack_walls_defenders_sally`
- `castle_attack_walls_belfry`
- `castle_attack_walls_ladder`
- `custom_battle`

Excluded from battle continuation and takeover:

- `bandits_at_night`: it includes the legacy camera triggers, but its battle result still intentionally ends on `main_hero_fallen` or side elimination. Leave it as legacy free-camera behavior until the ambush flow is explicitly redesigned.
- `prison_break`, tutorial missions, arena/duel missions, training missions, and scripted companion/set-piece missions: these are designed around a specific player body or scripted failure state.

Current player-fall behavior:

- The safe battle templates now allow victory after the player falls, record the second-in-command outcome once, and clear post-defeat state on practical finish paths.
- Immediate `main_hero_fallen` mission endings remain intentional in excluded mission families such as prison breaks, tutorials, training, arenas/duels, night ambushes, and scripted companion trials.
- No mission is currently classified as safe takeover. Hero takeover remains a future opt-in layer only.

## Player-Agent And Fall-Defeat Audit

Original player-agent assumptions found:

- Formation command triggers in `_preamble/00_imports.py` read `get_player_agent_no` and use the player team or player kill count. These are now gated with `neg|main_hero_fallen` where they issue player-position-based orders or award player kill-count morale/artifact effects.
- `common_siege_refill_ammo` reads the player agent only to avoid refilling the player during siege ammo refresh; it remains safe because it is not a player-command fallback loop.
- Battle order-panel update scripts read the player team for display and are presentation-driven, not mission-result drivers.
- Banner/chest placement scripts read the player agent during battle start setup; they run before post-defeat continuation matters.
- Arena, training, tutorial, prison-break, town/village center, and scripted companion/set-piece missions still assume the original player body is the mission focus. They remain excluded from takeover and from the safe continuation set.

`main_hero_fallen` force-defeat assumptions found:

- The safe field/siege/custom battle templates no longer use player fall alone as the victory/defeat decision.
- `custom_battle_check_defeat_condition` waits for side elimination, not player fall.
- `common_siege_check_defeat_condition` marks `$pin_player_fallen` instead of ending immediately, preserving the siege question/retreat flow.
- Immediate player-fall endings are still intentional in excluded mission families: prison break, tutorials, training, arena/duel missions, night ambushes, village/town scene fights, and scripted companion/set-piece missions.

## Implementation Checklist

### Phase 0: Audit And Guardrails

- [x] List every mission template that currently includes `camera_trigger_1` through `camera_trigger_8`.
- [x] Classify each mission as safe spectator, safe command continuity, safe takeover, or excluded.
- [x] Confirm which missions currently end immediately on `main_hero_fallen`.
- [x] Confirm which missions intentionally continue after player fall.
- [x] Identify all scripts that assume the original player agent remains the active player agent.
- [x] Identify all scripts that force defeat when `main_hero_fallen` is true.
- [x] Reserve or define safe agent/troop slots for post-defeat focus tracking.
- [x] Add static checks so new post-defeat globals are initialized and cleared.

### Phase 1: Shared Spectator State

- [x] Add `$sod_post_defeat_state`.
- [x] Add `$sod_post_defeat_enabled`.
- [x] Add `$sod_post_defeat_focus_agent`.
- [x] Add `$sod_post_defeat_focus_index`.
- [x] Add `$sod_post_defeat_focus_count`.
- [x] Add `$sod_post_defeat_takeover_used`.
- [x] Add a shared init script for all post-defeat globals.
- [x] Add a shared clear script for mission end cleanup.
- [x] Call init from `ti_before_mission_start` in safe battle templates.
- [x] Call clear from mission-end paths where practical.

### Phase 2: Watchable Agent Selection

- [x] Add `script_sod_post_defeat_agent_is_watchable`.
- [x] Treat alive allied heroes as highest-priority watch targets.
- [x] Treat alive allied captains/officers as second-priority watch targets.
- [x] Treat regular allied agents as fallback targets.
- [x] Exclude dead, non-human, invalid, routed, scripted-only, or forbidden agents.
- [x] Rebuild the focus list when the player first falls.
- [x] Rebuild the focus list when reinforcements arrive after player fall.
- [x] Rebuild the focus list when the focused agent dies or becomes invalid.
- [x] Ensure no enemy agent becomes watch focus unless explicitly allowed.

### Phase 3: Camera Follow Upgrade

- [x] Keep the existing free-camera controls working.
- [x] Add a follow-camera mode that tracks `$sod_post_defeat_focus_agent`.
- [x] Add input to cycle to the previous focus target.
- [x] Add input to cycle to the next focus target.
- [x] Show the focused agent name when the focus changes.
- [x] Auto-switch to the next valid focus when the current focus dies.
- [x] Fall back to free camera if no valid focus target remains.
- [x] Avoid repeatedly displaying long tutorial text.
- [x] Add a short first-time help message for the post-defeat controls.
- [x] Ensure Tab/retreat behavior still works.

### Phase 4: Battle Result Safety

- [x] Ensure player fall alone does not force defeat in spectator-safe missions.
- [x] Ensure all enemies defeated still counts as victory even if the player is down.
- [x] Ensure all allies defeated still counts as defeat.
- [x] Ensure casualty counting runs once and only once.
- [x] Ensure `$pin_player_fallen` or equivalent state does not block victory.
- [x] Verify battle continuation does not break reinforcement triggers.
- [x] Verify formation/order scripts do not spam orders after player fall.

### Phase 5: Command Continuity

- [x] Add `$sod_post_defeat_second_in_command`.
- [x] Define second-in-command eligibility.
- [x] Prefer designated officers or companions over arbitrary heroes.
- [x] Require the officer to be alive and present in the mission.
- [x] Apply a morale shock when the player falls.
- [x] Reduce morale shock if a qualified officer survives.
- [x] Increase rout risk if no officer survives.
- [x] Record which troop held command after the player fell.
- [x] Feed the result into battle ranking or company memory.
- [x] Surface command-continuity memory in companion/company reports.

### Phase 6: Optional Hero Takeover Prototype

- [x] Audit Custom Commander's pre-battle commander selection.
- [x] Add a pre-battle acting commander selector.
- [x] Gate battle entry on the selected acting commander rather than only `trp_player`.
- [x] Spawn the real player as an allied AI agent when a companion leads.
- [x] Use a dismounted player-ally spawn for sieges and tight village scenes.
- [x] Restore the real player's battle health once in the debrief.
- [x] Reset acting commander state on map-free.
- [x] Preserve the stricter post-defeat takeover prototype as a separate future opt-in.
- [ ] Add `$sod_post_defeat_mission_allows_takeover`.
- [ ] Add `script_sod_post_defeat_agent_is_controllable`.
- [ ] Require mission opt-in before takeover is possible.
- [ ] Require the focused agent to be allied.
- [ ] Require the focused agent to be a living human hero.
- [ ] Require the focused troop to be in `p_main_party`.
- [ ] Block takeover during duels, prison breaks, tutorials, scripted trials, and scene conversations.
- [ ] Store the original player troop before calling `set_player_troop`.
- [ ] Store the original focused agent and troop.
- [ ] Validate a safe spawn position near the focused agent.
- [ ] Spawn the new player-controlled agent only after all checks pass.
- [ ] Restore horse/equipment state safely if the chosen hero is mounted.
- [ ] Copy only known safe agent slots.
- [ ] Remove or hide the old AI agent only after the new agent is valid.
- [ ] Set `$sod_post_defeat_takeover_used` so takeover is once per battle.
- [ ] Restore the original player troop after the mission.
- [ ] Record takeover use in companion/company memory.

### Phase 7: Presentation And Feedback

- [x] Decide whether the first version needs a presentation or only messages.
- [ ] If using a presentation, keep it smaller than 108-WB's `choose_fighter_in_battle`.
- [ ] Show only valid command candidates.
- [ ] Display why takeover is unavailable when blocked.
- [x] Avoid using debug or placeholder wording.
- [x] Add post-battle summary text for who took command.
- [x] Add event text for no surviving officer.
- [x] Add event text for victory after the captain fell.
- [x] Add event text for collapse after the captain fell.

### Phase 8: Tests And Static Checks

- [x] Add a static test that shared spectator/follow-camera wiring exists.
- [x] Add a static test that custom battle defeat waits for side elimination, not player fall.
- [x] Add a static test that safe battle templates initialize post-defeat state.
- [x] Add a static test that excluded mission templates do not include takeover triggers.
- [ ] Add a static test that takeover is gated by `$sod_post_defeat_mission_allows_takeover`.
- [ ] Add a static test that original player troop restore logic exists.
- [x] Add a static test that no broad pasted 108-WB trigger block was copied into multiple templates.
- [x] Run `py build\test_feature_audit_static.py`.
- [x] Run `py build\doctor.py`.
- [x] Run `py build\build_all.py`.

### Phase 9: Manual Playtest Matrix

- [ ] Field battle: player falls, allies win.
- [ ] Field battle: player falls, allies lose.
- [ ] Field battle: player falls, reinforcements arrive.
- [ ] Field battle: focused companion dies, camera switches.
- [ ] Siege attack: player falls on ladder/wall.
- [ ] Siege defense: player falls, defenders continue.
- [ ] Village raid: player falls, battle resolves correctly.
- [ ] Bandit attack: player falls with no companion alive.
- [ ] Custom battle: spectator camera remains stable.
- [ ] Excluded duel mission: player fall ends normally.
- [ ] Excluded prison break: player fall ends normally.
- [ ] Optional takeover battle: eligible companion can take command.
- [ ] Optional takeover battle: ineligible troop is blocked with clear feedback.
- [ ] Optional takeover battle: player troop restores after mission.
- [ ] Save/load after battle does not preserve stale post-defeat globals.
