# Looter Village Raids Design And Implementation Checklist

This document turns looters from early-game background clutter into a light regional security threat. The goal is not to make looters behave like lords or trained armies. The goal is to let ignored road banditry grow into village fear, food loss, and local disorder.

Looters should remain opportunists. They raid slowly, break easily, and avoid real soldiers. If a ruler keeps roads patrolled, looters stay a nuisance. If a region is neglected, a large mob can gather enough courage to threaten a nearby village.

## Design Goals

- Keep looters relevant after the first few campaign weeks.
- Create small emergent village-defense stories without adding a new faction war layer.
- Give patrols, companions, militia, and local lord response more purpose.
- Make road security visibly matter to prosperity, food, and village safety.
- Avoid punishing one faction forever just because a looter spawn point is nearby.
- Avoid letting looters raze the map like organized lord parties.

## Core Fantasy

Looters begin as scavengers and road thieves. If ignored, several bands may swell into a desperate mob. Once the mob is large enough and the local region looks weak, it can attempt a crude raid against a village.

The raid is messy and inefficient:

- Looters prefer isolated or poorly protected villages.
- Looters avoid strong nearby lord parties, patrols, garrisons, and player forces.
- Looters take longer than lords to complete a raid.
- Looters inflict partial economic and safety damage rather than reliably burning the village.
- Looters abandon the raid if a serious threat approaches.
- Looters may scatter, shrink, or lose morale after a failed raid.

## Threat Stages

Use staged behavior so the feature escalates naturally:

- **Scavengers:** small looter parties using normal road-bandit behavior.
- **Gang:** medium looter parties that are more willing to chase farmers, refugees, and weak caravans.
- **Mob:** large looter parties that can consider village targets.
- **Raid Host:** a large mob actively moving to or plundering a village.

Implemented first-pass thresholds:

- Scavengers: fewer than 18 troops.
- Gang: 18 to 44 troops.
- Raid-capable mob: 45 or more troops after campaign day 30.
- Raid Host: a raid-capable `pt_bandits` mob that has passed the eligibility and target-selection guards.

These values should be difficulty-scaled in a later pass after live campaign testing against SoD's faster party-size growth.

## Target Selection

A looter mob should only raid when a target is plausible.

Valid target requirements:

- Target is a village.
- Village is not already looted, raided, under siege, or hidden behind an invalid state.
- Village is within a reasonable radius of the looter party.
- Village is not protected by a strong nearby lord party, patrol, garrison, or player-owned external force.
- Village is not on looter-raid cooldown and the target faction is not already at the active looter-raid cap.
- Global active looter raid cap has room.
- Campaign day is beyond the early grace period unless difficulty explicitly allows early raids.

Target preference:

- Isolated villages.
- Villages with low prosperity, low militia, low relation, or low security.
- Villages recently hit by caravans being destroyed nearby.
- Villages near looter spawn regions.
- Villages with no friendly patrol or lord nearby.

Target avoidance:

- Villages near castles or towns with active defenders.
- Villages near the player's army if the player is strong.
- Villages recently defended from a looter raid.
- Villages belonging to a faction already suffering too many recent looter raids.

## Balance Guardrails

The system must not create a permanent punishment loop for one unlucky faction.

- Add a village cooldown after any looter raid attempt.
- Add a village cooldown after successful defense, failed raid, or completed raid.
- Add a global active raid cap, probably 1 to 3 depending on campaign difficulty and day.
- Add a faction pressure cap so one faction cannot receive all active looter raids.
- Add an early-game grace period, recommended day 20 or day 30.
- Make looter raids slower than lord raids.
- Make looter raids less destructive than lord raids.
- Make looters more likely to flee than commit if a proper army approaches.
- Let patrols and local lords treat active looter raids as high-priority threats.
- Prevent looter parties from chaining one raid into another without recovery time.

## Raid Outcomes

Use partial outcomes instead of binary village destruction.

Possible success effects:

- Reduce village prosperity slightly.
- Reduce village food stores or market supply.
- Reduce local security.
- Add temporary village fear/unrest.
- Reduce available recruits for a short period.
- Spawn refugee, farmer, or elder complaint dialogue.
- Increase nearby lord concern or patrol priority.

Possible failure effects:

- Looters lose troops or morale.
- Looter party may split or scatter.
- Village gains a short defense cooldown.
- Player gains village relation, honor, renown, or local gratitude if involved.
- Patrol/lord defender may gain local security credit if the player was not involved.

Avoid first-pass effects that are too harsh:

- Do not fully raze a village by default.
- Do not permanently destroy improvements.
- Do not create lord-war raid states unless the engine already safely supports that distinction.
- Do not let looters capture villages or hold prisoners at village scale in v1.

## World Feedback

The feature should be visible without becoming spammy.

Light reports:

- "A large band of looters has been seen gathering near {s1}."
- "Looters have begun plundering around {s1}."
- "Villagers from {s1} say the roads are no longer safe."
- "A patrol has turned toward {s1} after reports of looters."
- "The looters at {s1} scattered before a proper force arrived."

Dialogue hooks:

- Village elders can mention looter pressure.
- Guild masters can mention unsafe roads.
- Companions with security, mercy, trade, or discipline themes can comment.
- Patrol captains can report recent looter activity.

Player-facing restraint:

- Show nearby or relevant reports.
- Avoid global spam for every minor looter movement.
- Prefer messages for active raids, successful defense, or serious regional escalation.

## AI Shape

Use a lightweight periodic script, not a full lord AI replacement.

Recommended flow:

1. Periodically scan looter parties.
2. Skip invalid, tiny, already-engaged, fleeing, or recently processed parties.
3. Estimate looter threat stage from party size and campaign day.
4. If the party qualifies as a mob, find a valid nearby village.
5. Score target villages by vulnerability and regional cooldown.
6. If a target is selected, assign looter raid state slots.
7. Move the looter party toward the target village.
8. Once near the village, enter a slow plundering state.
9. Apply small periodic damage while the raid continues.
10. Interrupt the raid if defenders arrive or looters lose enough strength.
11. Resolve success, failure, or abandonment and set cooldowns.

## Suggested State

Party slots:

- `slot_party_sod_looter_raid_state`
- `slot_party_sod_looter_raid_target`
- `slot_party_sod_looter_raid_start_time`
- `slot_party_sod_looter_raid_last_tick`
- `slot_party_sod_looter_raid_origin_region`
- `slot_party_sod_looter_recently_checked`

Village slots:

- `slot_center_sod_looter_raid_cooldown_until`
- `slot_center_sod_looter_raid_pressure`
- `slot_center_sod_looter_last_raid_day`
- `slot_center_sod_looter_last_defense_day`
- `slot_center_sod_security_pressure`
- `slot_center_sod_looter_player_reward_cooldown_until`

Globals:

- `$g_sod_active_looter_raids`
- `$g_sod_last_looter_raid_report_day`
- `$g_sod_looter_raid_grace_until_day`

Constants:

- `sod_looter_raid_state_none`
- `sod_looter_raid_state_gathering`
- `sod_looter_raid_state_moving_to_target`
- `sod_looter_raid_state_plundering`
- `sod_looter_raid_state_fleeing`
- `sod_looter_raid_state_resolving`

## Implementation Checklist

### Audit

- [x] Find all looter spawn scripts and party templates.
- [x] Find current looter AI assignment and behavior refresh scripts.
- [x] Find village raid, village prosperity, food, and recovery scripts.
- [x] Find lord/patrol reaction scripts for raided villages.
- [x] Find farmer/refugee/caravan party interaction with looters.
- [x] Find existing bandit lair or bandit-party escalation systems, if any.
- [x] Find map-message/report conventions for regional incidents.
- [x] Confirm which party templates count as looters and which are bandits/deserters.

Audit source map:

- Generic looter spawning: `src/scripts/ZZ_common_array_processing/spawn_bandits.py` spawns `pt_bandits`; `src/triggers/ST04_weekly/entry_0105.py` can also create desperation `pt_bandits`; merchant/mayor quest paths and several RTC campaign helpers create quest-specific `pt_bandits`.
- Other outlaw spawning: `spawn_bandits.py`, `script_sod_lord_party_morale.py`, and `script_sod_company_accounts.py` create mountain/forest/steppe/sea bandits and deserter parties. See `docs/reports/looter_bandit_deserter_economy_audit.md` for the broader pressure audit.
- Current bandit AI: `spawn_bandits.py` assigns generic `pt_bandits` to `spai_raiding_around_center`, `spai_patrolling_around_center`, or `spai_holding_center`; `script_party_set_ai_state` centralizes those map-AI behaviors; `script_sod_process_looter_village_raids` now layers the looter-village raid state on top without using native lord raid state.
- Village war raid/recovery: `script_process_village_raids`, `script_village_set_state`, `script_process_hero_ai`, and village menus handle native `svs_being_raided` / `svs_looted`; the looter system deliberately avoids those states.
- Economy/food/prosperity: village population/prosperity/food hooks live across `update_center_population_supply.py`, `sod_get_center_food_profile`, `sod_get_center_security_profile`, `center_get_food_consumption.py`, `change_center_prosperity.py`, `refresh_village_defenders.py`, and weekly economy triggers.
- Lord/patrol response: `process_hero_ai.py`, `kingdom_hero_decide_next_ai_state.py`, `sod_find_castle_patrol_threat_target.py`, and `sod_process_castle_patrols.py` are the key response points; looter raid hosts now get patrol priority and cautious nearby defender redirection.
- Farmer/refugee/caravan interaction: `create_village_farmer_party.py`, caravan AI/trade scripts, `cf_sod_party_is_hostile_economy_party.py`, `sod_apply_hostile_noncombat_economy_effects.py`, and hostile encounter dialogue determine how outlaw parties pressure noncombat map parties.
- Bandit escalation/lair adjacent systems: threat-board archetype scripts, hideout clue helpers, hostile economy/reputation helpers, and prisoner-economy breakout bandit spawns already create broader outlaw escalation surfaces.
- Map-message conventions: nearby/relevant messages use `display_message` with muted colors; kingdom-scale events use `display_log_message`, `script_add_notification_menu`, or `script_add_log_entry`. Looter raids use nearby `display_message` only in v1.
- Template classification for this feature: only `pt_bandits` counts as looters eligible for village raids. Mountain/forest/steppe/sea raiders are bandits, while `pt_deserters`, `pt_sod_deserters`, and `pt_sod_merc_deserters` are deserters. `pt_bandits_awaiting_ransom` is quest-only and excluded.

### Constants And Slots

- [x] Add looter raid state constants.
- [x] Add looter raid party slots.
- [x] Add village looter pressure/cooldown slots.
- [x] Add global active-raid tracking.
- [x] Add defaults during game start or old-save repair.
- [x] Document all new slot ranges in slot allocation docs if required.

Implemented constants and slots:

- Party slots: `slot_party_sod_looter_raid_state`, `slot_party_sod_looter_raid_target`, `slot_party_sod_looter_raid_start_time`, `slot_party_sod_looter_raid_last_tick`, `slot_party_sod_looter_raid_origin_region`, `slot_party_sod_looter_recently_checked`.
- Village slots: `slot_center_sod_looter_raid_cooldown_until`, `slot_center_sod_looter_raid_pressure`, `slot_center_sod_looter_last_raid_day`, `slot_center_sod_looter_last_defense_day`, `slot_center_sod_security_pressure`, `slot_center_sod_looter_player_reward_cooldown_until`.
- Globals: `$g_sod_active_looter_raids`, `$g_sod_last_looter_raid_report_day`, `$g_sod_looter_raid_grace_until_day`.
- Constants: `sod_looter_raid_state_*`, grace/min-size/global-cap/cooldown/radius/tick/pressure/report tuning values.

### Eligibility

- [x] Add `script_cf_sod_looter_party_can_consider_village_raid`.
- [x] Require looter or approved low-tier bandit party type.
- [x] Require minimum party size.
- [x] Respect early-game grace period.
- [x] Skip parties already in battle, fleeing, quest-locked, attached, or invalid.
- [x] Skip parties currently assigned to a non-looter special behavior.
- [x] Skip parties recently processed to avoid expensive repeated scans.

Implemented eligibility behavior:

- Only `pt_bandits` currently qualifies; future low-tier bandit templates should be explicitly added rather than inferred from faction alone.
- Candidate parties must be active, unattached, outside towns, out of battle, above the minimum size, past the campaign grace period, and not flagged by SoD threat quest state.
- Parties retreating to a center, carrying the retreat flag, or assigned to non-looter AI states are ignored so this system does not steal parties from quest, combat, or special behavior.
- The per-party recently checked slot throttles expensive scans.

### Target Selection

- [x] Add `script_sod_looter_find_village_raid_target`.
- [x] Score nearby villages by distance, protection, prosperity, recent raids, and isolation.
- [x] Reject invalid village states.
- [x] Reject villages protected by strong nearby armies or patrols.
- [x] Reject villages under cooldown.
- [x] Reject factions above recent looter pressure cap.
- [x] Prefer villages with low security or low patrol coverage.
- [x] Add safe fallback behavior when no target is valid.

Implemented target behavior:

- Candidate villages must be active, normal-state villages, not infested, in range, and off looter-raid cooldown.
- Candidate raid villages must have at least one actual defender or militia volunteer, so looters do not start a village assault against an empty party. Separate population-desperation spawns may still originate from a collapsing village, but those village-origin parties are rebuilt as looter-only bands rather than mixed bandits.
- Strong nearby player, lord, patrol, player patrol, and player mercenary forces reject the village outright.
- Existing active looter raids against the same target faction count against the looter raid cap to prevent one faction from being dogpiled by independent looter mobs.
- The score favors nearby, vulnerable, low-security, low-patrol villages and penalizes existing pressure plus recent raids or recent defenses.
- If no legal target exists, the script returns `reg0 = -1` and no raid is assigned.

### Raid Assignment

- [x] Add `script_sod_looter_assign_village_raid`.
- [x] Store target center on the looter party.
- [x] Set looter raid state to moving-to-target.
- [x] Increment active looter raid count safely.
- [x] Set party AI toward the target village.
- [x] Add a short report if the player is nearby or has local interest.
- [x] Avoid overwriting lord, quest, or external-party AI.

Implemented assignment behavior:

- Assignment revalidates the party and target instead of trusting the caller.
- Only `pt_bandits` in an idle looter-compatible AI state can be assigned.
- Lord parties, player patrols, player mercenary companies, quest-threat parties, attached parties, battle parties, and retreating parties are rejected defensively.
- Active raid count is clamped to the configured cap after assignment.
- The party stores the target village and moves toward it with looter raid state, AI state, and AI object all aligned.

### Plundering Behavior

- [x] Add `script_sod_looter_raid_tick`.
- [x] Detect arrival near target village.
- [x] Transition moving-to-target into plundering.
- [x] Apply slow periodic village pressure while plundering.
- [x] Reduce food, prosperity, or recruit availability modestly.
- [x] Use pressure stages rather than instant full village loot.
- [x] Check for defenders every tick.
- [x] Abort if looters are too weak, target becomes invalid, or defenders arrive.

Implemented plundering behavior:

- Arrival within `sod_looter_raid_arrival_distance` switches the party from travel AI to a small patrol around the village.
- Pressure rises every `sod_looter_raid_tick_hours`, softened by village security/resistance.
- Crossing pressure stages damages the village gradually: low pressure reduces food stores, mid pressure also trims volunteers, and high pressure adds minor local prosperity damage.
- Each tick validates the village, looter strength, and defender presence before applying more pressure.

### Resolution

- [x] Add `script_sod_looter_resolve_village_raid`.
- [x] Resolve success with partial village damage.
- [x] Resolve failure with looter losses, scatter chance, and village defense cooldown.
- [x] Resolve abandonment without heavy village damage.
- [x] Decrement active looter raid count safely.
- [x] Clear party raid slots.
- [x] Set regional and village cooldowns.
- [x] Add player-facing reports only for meaningful outcomes.

Implemented resolution behavior:

- Success never uses the vanilla full-loot village state; it applies partial prosperity, local prosperity, volunteer, and security pressure damage.
- Defense clears pressure, applies a defense cooldown, lowers security pressure slightly, removes looter casualties, and has a chance to scatter extra looters.
- Abandonment clears the raid with only a short cooldown and minor security concern, avoiding heavy damage when the target became invalid or looters became too weak.
- All outcomes clear looter raid slots, reset party AI state, and decrement active raid count safely.
- Nearby reports are limited to meaningful success or defense outcomes.

### Defender Response

- [x] Make local patrols prioritize active looter raids.
- [x] Let nearby lord parties consider intercepting active looter raid hosts.
- [x] Let player-owned external patrols respond if their patrol radius includes the village.
- [x] Ensure response AI does not break existing patrol/follower-party orders.
- [x] Add a low-cost village militia resistance check if no defender arrives.
- [x] Avoid making every nearby lord permanently chase tiny looter parties.

Implemented defender response behavior:

- Castle patrol targeting scores active looter raid hosts higher when the target village is inside the patrol region.
- Nearby lord parties only redirect when they are idle-compatible, uncommanded, close enough, and strong enough relative to the looter host.
- Player-owned patrols can respond only if the target village falls within their stored patrol radius.
- Player mercenary follower companies are not automatically redirected by this village-defense hook.
- High village resistance can occasionally scatter a weak/early plundering raid without spawning an expensive defender party.

### Player Interaction

- [x] Add nearby raid-start message.
- [x] Add village elder dialogue for active or recent looter pressure.
- [x] Add reward logic for interrupting a looter raid.
- [x] Add relation/renown/honor reward tuning.
- [x] Add companion comment hooks for mercy, discipline, trade, and security personalities.
- [x] Add map report line for defended villages.
- [x] Avoid forcing a quest unless a later design intentionally adds one.

Implemented player interaction behavior:

- Nearby raid-start and plundering messages are map reports, not forced quests.
- Village elders expose active pressure and recent raid/defense memory through dialogue; old incidents age out after a bounded recent window.
- Player interruption resolves as defense, grants a small village relation, renown, and honor reward, and is throttled by a per-village reward cooldown.
- Companion relationship hooks fire for village help, roadcraft/security, food security, public security, and orderly trade outcomes; Ymira, Bunduk, and Marnid can add light flavor lines when present.
- Defended-village reports are shown only when the player is near enough to plausibly hear them.

### Economy And Village Effects

- [x] Decide exact prosperity damage range.
- [x] Decide exact food/security/recruit pressure range.
- [x] Prevent looter raids from stacking too much with war raids.
- [x] Add recovery decay for looter pressure.
- [x] Make repeated neglect visible but not catastrophic.
- [x] Keep recovery possible through patrols, quests, or time.

Implemented economy tuning:

- Pressure stages apply modest plundering damage before final resolution: food store loss of 18/36/54, one volunteer loss at mid pressure, and one local prosperity loss at high pressure.
- Successful raids add only partial final damage: -4 town prosperity, -3 local prosperity, -2 volunteers, and +12 security pressure.
- Defense reduces security pressure by 4 and sets a shorter defense cooldown; abandonment adds only +2 security pressure and a short cooldown.
- Looter raids never set `svs_looted` and do not call `script_village_set_state`.
- If a village enters a non-normal state from war or another system before resolution, the looter raid resolves as abandonment instead of stacking damage.
- Looter pressure and security pressure decay over time, with patrol/defense systems able to accelerate practical recovery by stopping active raids.

### Edge Cases

- [x] Looter target village becomes looted by a lord before looters arrive.
- [x] Looter party is defeated while moving to target.
- [x] Looter party is defeated while plundering.
- [x] Player joins battle against looters during plundering.
- [x] Player loses to looters during plundering.
- [x] Village changes faction during looter raid.
- [x] Nearby siege begins while looters are raiding.
- [x] Looter party merges, splits, or receives reinforcements during raid state.
- [x] Save/load occurs while looters are plundering.
- [x] Active raid count becomes desynced from actual parties.
- [x] Old saves lack new slots.
- [x] Looter raid target gets deleted or disabled.

Implemented edge-case behavior:

- If the target village leaves normal village state, becomes inactive, changes faction, or becomes besieged, the raid resolves as abandonment rather than stacking damage.
- Active raid hosts defeated by player or autoresolve are resolved as defended raids before their party state is cleared.
- If the player loses to an active raid host, the raid state remains intact and the host continues unless later checks make it too weak or invalid.
- Reinforcement or loss changes are tolerated; parties below the weakness threshold abandon, while larger parties continue without generating extra rewards, prisoners, or recruits.
- Save/load repair clears stale old-save slots, initializes missing original-faction metadata, clamps pressure, and recomputes the active raid count from real parties.

### Exploit Controls

- [x] Prevent farming infinite village relation from repeated looter raid defense.
- [x] Add reward cooldown per village.
- [x] Prevent player from baiting looters into constant low-risk reward loops.
- [x] Prevent looter raids from generating infinite recruits, loot, or prisoners.
- [x] Prevent looter raid parties from becoming valid external follower parties.
- [x] Prevent looter raid parties from being selected as unrelated quest targets.
- [x] Prevent active raid hosts from ignoring battle outcomes.

Implemented exploit controls:

- Defense rewards are throttled by village reward cooldown, minimum looter size, global active cap, village cooldown, and conservative target selection.
- The looter raid scripts never add troops, prisoners, loot, or recruits to the player; they only adjust village pressure/recovery state.
- Active raid hosts keep ordinary looter party type and are explicitly rejected by external follower command gates.
- Active raid hosts are marked by dedicated raid slots and are resolved/cleared before battle cleanup, preventing stale defeated raiders from continuing to pressure a village.
- Quest-spawned and special-behavior parties are skipped by eligibility and assignment guards, and active looter raid slots give future quest-target selectors a clear exclusion point.

### Static Tests

- [x] Add `build/test_looter_village_raids_static.py`.
- [x] Assert looter raid constants and slots exist.
- [x] Assert target selection rejects protected or invalid villages.
- [x] Assert early-game grace period is checked.
- [x] Assert global active-raid cap is checked.
- [x] Assert village and regional cooldowns are checked.
- [x] Assert raid assignment stores party state and target.
- [x] Assert raid resolution clears state and decrements active raid count.
- [x] Assert player-facing reports are throttled.
- [x] Assert looter raids do not use lord raid behavior directly unless explicitly wrapped.

Implemented static coverage:

- `build/test_looter_village_raids_static.py` covers slots/constants, trigger hookup, eligibility, target selection, assignment, staged plundering, resolution, defender response, player interruption, elder dialogue, edge-case repair, and exploit controls.
- Static checks verify looter raids do not call `script_village_set_state`, do not use `svs_looted`, and do not add troops or prisoners to the player.
- Static checks verify active raid hosts are resolved before autoresolve clears defeated parties.

### Manual QA

- [ ] Start a new campaign and confirm no immediate looter village raids during grace period.
- [ ] Spawn or grow a large looter party and confirm it can select a weak village.
- [ ] Confirm looters avoid a village protected by a nearby lord or patrol.
- [ ] Confirm looters begin slow plundering when they reach the village.
- [ ] Confirm player interruption resolves as defense, not normal unrelated bandit cleanup.
- [ ] Confirm patrol interruption resolves correctly.
- [ ] Confirm successful looter raid causes modest village damage, not full devastation.
- [ ] Confirm repeated raids respect cooldowns.
- [ ] Confirm save/load during active raid repairs or preserves state correctly.
- [x] Confirm full build and doctor pass after implementation.

Manual QA note:

- The remaining unchecked items require an in-game campaign/session because they depend on live map AI, encounters, save/load, and visual player-facing reports. Static/build coverage is complete for this pass.

## Recommended First Pass

Implement the smallest reliable version first:

- [x] One global active looter raid at a time.
- [x] Day 30 grace period.
- [x] Minimum 45 looters.
- [x] Village cooldown of 14 days.
- [x] Faction pressure cap of one active looter raid.
- [x] Partial damage only: prosperity, food/security pressure, and recruit delay.
- [x] Nearby player report only.
- [x] Patrol/lord response added after the raid state is stable.

This gives the system life without letting it eat the campaign map.

## Implementation Notes

First-pass implementation lives in `src/scripts/ZY_helper_scripts/sod_looter_village_raids.py` and is driven by `src/triggers/ST02_every_hour/entry_0168.py`.

The system deliberately does not call `script_village_set_state` or use `svs_looted`; looters apply separate pressure, cooldown, modest prosperity/local prosperity damage, recruit pressure, and village elder dialogue. Player interruption resolves the raid as a defense and grants a small relation/renown/honor reward.

Patrol and lord response is intentionally conservative: active looter raid hosts receive priority in castle patrol target scoring, and only nearby non-critical defenders with enough strength are redirected toward the raid host.

Exploit and recovery controls now include a per-village player reward cooldown, old-save/state repair for active looter raid slots, pressure clamping, and gradual decay for looter pressure and security pressure.
