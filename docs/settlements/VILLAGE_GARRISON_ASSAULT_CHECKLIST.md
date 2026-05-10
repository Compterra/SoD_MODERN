# Village Garrison Assault Checklist

This document extends the looter village raid system so a village raid feels physically real. A raid should not move straight from "looters reached the village" to "looters are plundering." First, the raiders must break the village's local defenders.

The village garrison already exists as actual troop stacks in the village party. This pass makes those defenders matter at the moment a raid begins.

## Design Goal

When a looter raid host reaches a village, the first event should be an assault against the village garrison and militia. If the defenders hold, the raid fails. If the raiders win, the village enters plundering with defender losses, militia losses, and pressure based on how costly the assault was.

This should remain lightweight for AI-only raids. The player should only see a battle scene when they personally intervene. Otherwise, use autoresolve with real troop counts, village security, militia, buildings, and nearby support.

## Existing Village Defense Model

Village defense currently has three layers:

- **Village garrison:** actual troops inside the village party, counted with `party_get_num_companions(village)`, refreshed by `script_refresh_village_defenders`, and added from `pt_village_defenders`.
- **NPC militia pool:** `slot_center_npc_volunteer_troop_amount/type`, used by security and faction power.
- **Player recruit pool:** `slot_center_volunteer_troop_amount/type`, used for player recruitment and separate from the garrison.

The assault should primarily use the first two. The player recruit pool should only be damaged as a later village-pressure effect, not treated as the first line of defense.

## Desired Flow

1. Looter raid host reaches its target village.
2. Raid logic validates that the village is still a valid target.
3. New garrison assault script resolves the initial fight.
4. If defenders win:
   - raid resolves as failed;
   - looters take losses or scatter;
   - village gets a defense cooldown;
   - nearby/relevant player message may fire.
5. If raiders win:
   - actual village garrison is reduced;
   - NPC militia pool is reduced;
   - looter party takes casualties proportional to resistance;
   - raid enters plundering state;
   - initial looter pressure is set based on the assault result.
6. Plundering continues through the existing looter raid tick.

## Assault Outcome Grades

Use simple grades instead of binary success so reports and consequences feel believable.

- **Defender rout:** defenders win clearly; looters lose troops and abandon the raid.
- **Defender hold:** defenders barely hold; looters fail, village suffers small militia/garrison losses.
- **Costly raider success:** looters win, but lose enough troops that plundering starts slowly or may still be interrupted easily.
- **Clean raider success:** looters win with moderate losses; normal plundering begins.
- **Overwhelming raider success:** looters crush a weak village; plundering starts with higher pressure, but still should not instantly loot the village.

## Implementation Checklist

### Constants And Slots

- [x] Add `sod_looter_raid_state_assaulting` between moving-to-target and plundering, if a distinct state is useful.
- [x] Add assault result constants:
  - [x] `sod_village_assault_result_defender_rout`
  - [x] `sod_village_assault_result_defender_hold`
  - [x] `sod_village_assault_result_raider_costly`
  - [x] `sod_village_assault_result_raider_clean`
  - [x] `sod_village_assault_result_raider_overwhelming`
- [x] Add `slot_party_sod_looter_raid_assault_resolved`, or equivalent, if the existing state transition needs protection from duplicate resolution.
- [x] Add `slot_center_sod_looter_last_assault_day`.
- [x] Add `slot_center_sod_looter_last_assault_result`.
- [x] Add `slot_center_sod_looter_garrison_losses_recent`.
- [x] Add `slot_center_sod_looter_militia_losses_recent`.
- [x] Ensure old-save defaults treat missing assault slots as zero/none.

### Core Assault Script

- [x] Add `script_sod_looter_resolve_village_garrison_assault(looter_party, target_village)`.
- [x] Validate `looter_party` is active.
- [x] Validate `target_village` is a village.
- [x] Reject looted, deserted, invalid, deleted, or faction-changed targets.
- [x] Reject assault if the looter party no longer has a valid looter raid state.
- [x] Read actual village garrison size from `party_get_num_companions(target_village)`.
- [x] Read NPC militia amount from `slot_center_npc_volunteer_troop_amount`.
- [x] Read village security profile through `script_sod_get_center_security_profile`.
- [x] Include looter party size and cached strength.
- [x] Include nearby defender pressure only as a modifier, not as a full battle unless those parties physically intercept.
- [x] Resolve the assault with deterministic enough math that save/load does not create wild variance.
- [x] Return result grade in `reg0`.
- [x] Return garrison losses in `reg1`.
- [x] Return militia losses in `reg2`.
- [x] Return looter losses in `reg3`.
- [x] Return starting plunder pressure in `reg4`.

### Casualty Application

- [x] Add `script_sod_apply_village_garrison_assault_losses(village, looter_party, garrison_losses, militia_losses, looter_losses)`.
- [x] Remove actual defender troops from the village party safely.
- [x] Prefer removing low-tier village defender stacks first unless code proves stack ordering is unreliable.
- [x] Never reduce village party stacks below zero.
- [x] Reduce NPC militia pool separately.
- [x] Do not directly reduce player recruit pool during the assault.
- [x] Apply looter losses to the looter party.
- [x] If looters fall below minimum viable raid size, resolve as failed even if they technically won the assault.
- [x] Store recent garrison/militia losses on the village for reports.
- [x] Avoid duplicating losses if the assault script is called twice in the same raid state.

### Looter Raid State Integration

- [x] Update `script_sod_looter_raid_tick`.
- [x] When a moving-to-target raid reaches arrival distance, call `script_sod_looter_resolve_village_garrison_assault`.
- [x] Only transition to `sod_looter_raid_state_plundering` if the raiders won the assault.
- [x] Resolve the raid as failed if defenders held.
- [x] Use `reg4` starting pressure when plundering begins.
- [x] Reset `slot_party_sod_looter_raid_last_tick` after assault resolution.
- [x] Prevent the existing arrival branch from immediately entering plundering without assault.
- [x] Ensure active raid count is decremented exactly once on failed assault.

### Autoresolve Formula

- [x] Build an assault score from looter strength, looter count, and looter party health.
- [x] Build a defense score from village garrison count, NPC militia count, center security, raid resistance, and patrol response.
- [x] Add a minimum defense floor so even tiny villages can bloody small looter bands.
- [x] Add a minimum raider floor so large but weak looter mobs are still dangerous.
- [x] Apply village building modifiers.
- [x] Apply prosperity/health modifiers carefully:
  - [x] high health improves defense reliability;
  - [x] low health increases militia losses;
  - [x] high prosperity improves preparedness modestly;
  - [x] low prosperity reduces staying power.
- [x] Use mild randomness only after the score gap is established.
- [x] Clamp all outcomes so no raid deletes an entire healthy village garrison in one lightweight assault.

### Building Effects

Keep building influence subtle. The assault should feel like a village's local preparation matters, not like each improvement is a separate combat perk. Most effects should flow through existing center modifier profiles: security, raid resistance, patrol response, warning range, garrison recovery, food security, health recovery, and population recovery.

Rules for building influence:

- [x] Use modifier profile totals instead of direct per-building assault checks wherever possible.
- [x] Let buildings nudge scores, losses, recovery, and warning reach rather than hard-deciding outcomes.
- [x] Avoid stacking many separate bonuses from the same building.
- [x] Avoid scene-specific claims unless the scene can actually show or imply the building.
- [x] Keep named-building dialogue as flavor only unless a direct hook is truly needed.

Existing village buildings should matter in small, readable ways:

- [x] **Watch Tower:** contributes through security, warning range, threat reduction, raid recovery, and patrol response. It should help notice and organize against raiders, not act like a wall.
- [x] **Messenger Post:** contributes through patrol response, security, construction coordination, and trade/news flow. It should improve warning and response more than raw defense.
- [x] **Manor:** contributes through administration, construction coordination, retention, population capacity, and modest recovery/renown hooks. It should make militia organization steadier, not stronger by itself.
- [x] **Mill / Granary:** contribute through food security, food storage, production, and recovery. They should improve endurance and post-raid recovery, but successful raiders may still value them as plunder targets.
- [x] **Shrine / Monastery:** contribute through faith stability, unrest reduction, health or population recovery, and administration. They should help morale/recovery softly, not become military buildings.
- [x] **Water Supply / Ambulatory:** contribute through health, disease resistance, population recovery, raid recovery, and food handling. They should reduce long-term harm more than immediate assault odds.
- [x] **Rustic Blacksmith / Clayworks:** contribute through tools, repairs, production, construction speed, and small security support. They should support recovery/preparedness without becoming fortifications.
- [x] **Inn:** contributes through trade, migration, retention, unrest reduction, and local news. It should help warning flavor and social cohesion, not combat strength.
- [x] **Militia Yard:** contributes through garrison recovery, recruit count/quality, security, and light raid resistance. It is the only new village building that should feel explicitly defensive in v1.
- [x] **Beacon Hill:** contributes through warning range, patrol response, security, threat reduction, and light bandit suppression. It should make raids harder to surprise, not harder to win once raiders are in the village.

### Optional Future Buildings

Only add these if the current building set needs more explicit village defense identity.

- [x] **Militia Yard:** implemented as a subtle modifier-first village defense building.
- [ ] **Palisade:** deferred. A real palisade should be visible or strongly implied in village scenes; do not implement it as a pure stat building.
- [x] **Beacon Hill:** implemented as a subtle modifier-first warning and response building.
- [x] **Militia Armory:** local arms store.
  - [x] Requires Rustic Blacksmith or Manor.
  - [x] Represents stored spears, shields, bows, repair tools, and levy gear rather than a fortified structure.
  - [x] Improves militia quality slightly through `recruit_tier_bonus_flat`, `garrison_recovery_flat`, and a small `security_flat` modifier.
  - [x] Does not add a large assault-defense bonus; it makes defenders better equipped, not harder to reach.
  - [x] If raiders win cleanly or overwhelmingly, they have a small chance to steal arms.
  - [x] Stolen arms briefly increase local security pressure instead of spawning a major army.
  - [x] Report flavor mentions stolen arms only after a raider victory.
- [ ] **Refuge Cellar:** noncombatant shelter.
  - [ ] Reduces population and volunteer losses.
  - [ ] Does not directly increase combat strength.
  - [ ] Helps make defensive villages feel prepared without turning every village into a fort.

### Reports And Dialogue

- [x] Add nearby message when looters begin the assault:
  - [x] "Looters have fallen on the militia of {s1}."
- [x] Add defender victory message:
  - [x] "The militia of {s1} drove off the looters before they could plunder the village."
- [x] Add costly defender victory message:
  - [x] "The defenders of {s1} held, though the village bury their dead by the road."
- [x] Add raider success message:
  - [x] "The defenders of {s1} have been broken. Looters are spreading through the lanes."
- [x] Add elder dialogue for recent assault losses.
- [x] Add elder dialogue if the village held because of strong buildings.
- [x] Add companion comment hooks for mercy, discipline, security, trade, and anti-bandit personalities.
- [x] Keep menus for reports/status only; use dialogue for human reaction.

### Player Interaction

- [x] If the player reaches the village before the garrison assault resolves, allow intervention against the looter party.
- [x] If the player defeats the looters before assault resolution, reward as prevention.
- [x] If the player defeats the looters after defenders are broken, reward as rescue but preserve village losses.
- [x] If the player loses to looters during active village assault/plunder, continue or resolve the raid according to looter strength.
- [x] Avoid giving repeated relation rewards from the same raid host.
- [x] Distinguish "saved before assault," "saved after costly assault," and "saved during plunder" in feedback.

### Recovery

- [x] Let `script_refresh_village_defenders` slowly rebuild garrison after assault if population allows.
- [x] Consider a temporary recent-loss penalty so daily refresh cannot instantly erase assault consequences.
- [x] Let Watch Tower, Manor, Monastery, Water Supply, Ambulatory, and Clayworks improve recovery.
- [x] Let high prosperity and health improve garrison recovery.
- [x] Let looted/deserted villages pause or sharply limit garrison recovery.
- [x] Preserve the existing population cost for new defenders.

### Balance Guardrails

- [x] Looter raids should still fail often against prepared villages.
- [x] Strong looter mobs should be able to beat weak villages.
- [x] A single looter raid should not annihilate every defender in a healthy village.
- [x] Assault losses should make future raids more dangerous if the region is neglected.
- [x] Buildings should help, but not make small villages immune forever.
- [x] Bound castles and patrols should matter through response and security, not by magically absorbing all assaults.
- [x] Lord raids should not accidentally use looter-only assault state unless intentionally extended later.

### Edge Cases

- [x] Target village becomes looted by a lord before looters arrive.
- [x] Target village changes faction before assault.
- [x] Looter party is defeated while moving to target.
- [x] Looter party is defeated during the assault window.
- [x] Looter party is too small after assault losses.
- [x] Village has zero garrison but some NPC militia.
- [x] Village has garrison but zero NPC militia.
- [x] Village has no defenders at all.
- [x] Village party has unexpected troop stacks.
- [x] Save/load occurs after arrival but before assault resolution.
- [x] Active raid count desyncs after failed assault.
- [x] Player joins a battle against looters while assault script is about to resolve.
- [x] Nearby defender AI is already assigned to another high-priority objective.
- [x] Existing village raid state `svs_being_raided` overlaps with looter raid pressure.

### Static Tests

- [x] Add `build/test_village_garrison_assault_static.py`.
- [x] Assert the looter arrival branch calls `script_sod_looter_resolve_village_garrison_assault`.
- [x] Assert moving-to-target no longer transitions directly to plundering without assault.
- [x] Assert village garrison count uses `party_get_num_companions(target_village)`.
- [x] Assert NPC militia uses `slot_center_npc_volunteer_troop_amount`.
- [x] Assert player recruit pool is not used as first-line assault defense.
- [x] Assert assault losses are applied to village garrison, NPC militia, and looter party.
- [x] Assert assault result is protected from duplicate application.
- [x] Assert Watch Tower and Messenger Post influence assault or response.
- [x] Assert resolve path decrements active raid count on defender victory.
- [x] Assert old looter village raid static tests still pass.

### Validation Commands

- [x] `py build\test_village_garrison_assault_static.py`
- [x] `py build\test_looter_village_raids_static.py`
- [ ] `py build\test_village_garrison_unification.py`
- [x] `py build\test_recruitment_garrison_modifiers.py`
- [x] `py build\doctor.py --doctor-new-only`
- [x] `py build\build_all.py`

## Recommended First Pass

Keep the first implementation subtle.

Use modifier profiles first:

- Security and raid resistance for the assault score.
- Warning range and patrol response for reports and defender response.
- Garrison recovery for post-assault rebuilding.
- Food security and health recovery for lower long-term harm.
- Population recovery/retention for slower post-raid collapse.

The current Phase 5 additions are enough for now:

- Militia Yard gives villages a modest dedicated defense identity without requiring scene edits.
- Beacon Hill improves warning/response without pretending the village has walls.
- Granary improves food security and recovery without changing the battlefield.

Do not add Palisade until village scenes can support it visually or narratively. A stat-only palisade would make the autoresolve math feel detached from what the player sees.
