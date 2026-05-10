# Interactive Quest Design

This document audits native Mount & Blade quest patterns from `References/Vanilla_Module_System` and converts them into a higher standard for companion quests in this mod.

The short version: our recent companion quest passes added better witnesses and branch consequences, but most of them are still too dialogue/menu-heavy. Native quests are interactive because they make the player move through the world, manipulate parties, enter scenes, protect or lose NPCs, fight, wait under pressure, and return to someone changed by the result.

## Native Quest Audit

### Quest State Is Stored Around World Objects

Native quests use `module_quests.py` for readable quest identity, but the real interactivity comes from slots in `module_constants.py`:

- `slot_quest_target_center`
- `slot_quest_target_troop`
- `slot_quest_target_party`
- `slot_quest_target_amount`
- `slot_quest_current_state`
- `slot_quest_giver_troop`
- `slot_quest_giver_center`
- `slot_quest_target_item`

The useful pattern is not just "quest stage = 1." It is "this quest has a target village, a spawned party, a named witness, a target amount, a current state, and cleanup rules."

Native lifecycle scripts in `module_scripts.py` also matter:

- `script_start_quest` writes date/giver/description notes, handles timeout notes, and starts the quest.
- `script_succeed_quest` and `script_fail_quest` mark success/failure but often still require a return conversation.
- `script_end_quest` clears quest notes and resets quest-offerer bookkeeping.
- `script_cancel_quest` clears notes and cancels without reward resolution.

Companion quests should follow the same separation:

- Start: companion opens the personal problem.
- Field test: a world object becomes active.
- Resolution: the player acts in the world.
- Report: the companion and witnesses react.
- Cleanup: spawned parties, pending globals, and witness flags are cleared.

### Ransom Girl

Native reference:

- `module_dialogs.py`: `qst_kidnapped_girl`
- `pt_bandits_awaiting_ransom`
- `pt_kidnapped_girl`

Interactive pieces:

- The quest spawns a bandit party near a target village.
- The player receives actual ransom money.
- Bandits can be paid, challenged, stalled, or attacked.
- The girl becomes a party/world object after release.
- The player can take her into the party, leave her waiting, lose her, or return her.
- Failure has specific social and financial consequences.

Design takeaway:

Companion quests should create vulnerable people, evidence, supplies, or enemy parties that exist outside the menu. If the player can lose the object, protect it, spend it, or betray it, the quest becomes memorable.

Companion translation:

- Ymira refugees should become a guarded refugee party or captive group.
- Jeremus wounded could become recoverable wounded/camp followers after battle.
- Firentis restitution could require escorted supplies or a guard detachment to a village.

### Train Peasants Against Bandits

Native reference:

- `module_game_menus.py`: `mnu_train_peasants_against_bandits`
- `mnu_train_peasants_against_bandits_ready`
- `mnu_train_peasants_against_bandits_attack`
- `mnu_train_peasants_against_bandits_success`
- `module_simple_triggers.py`: hourly training progression
- `mt_village_training`
- `mt_village_attack_bandits`

Interactive pieces:

- The player spends time training.
- Trainer skill changes preparation time.
- Training produces practice fights in the village scene.
- The training result updates quest progress.
- When enough peasants are trained, bandits attack.
- Final result changes village relation/state and offers a reward/refusal choice.

Design takeaway:

Native uses an activity loop before the climax. The player does not just pick "train peasants"; they invest time, fight practice rounds, then use that preparation in a real attack.

Companion translation:

- Lezalit's discipline quest should include a training/practice scene with troops.
- Matheld's line quest should include a shield-wall drill or post-battle hold-the-line fight.
- Bunduk's grievance could culminate in a defended watch, pay-line confrontation, or formation test.

### Collect Taxes

Native reference:

- `module_game_menus.py`: `mnu_collect_taxes`, `mnu_collect_taxes_revolt_warning`, `mnu_collect_taxes_revolt`
- `module_simple_triggers.py`: hourly tax collection
- `mt_back_alley_revolt`

Interactive pieces:

- The player commits to a timed collection process.
- Progress accumulates hour by hour.
- Skill, party size, and prosperity affect total time and income.
- A warning can appear before revolt.
- The player can halve taxes to reduce unrest.
- If pushed too far, a revolt mission starts.

Design takeaway:

Great interaction can come from pressure over time, not only combat. The important bit is interruption: the quest pushes back while the player is doing it.

Companion translation:

- Katrin's shortage quest should use ration/pay pressure over time, with a camp petition or desertion risk if ignored.
- Marnid's market quest should use price, debt, and reputation pressure rather than a single shop dialogue.
- Bunduk's pay grievance can escalate if wages are delayed after the witness.

### Hunt Down Fugitive

Native reference:

- `module_game_menus.py`: village center visitor setup
- `module_dialogs.py`: village elder/town dweller clue dialogue
- `module_mission_templates.py`: village/town mission triggers for fugitive death/player defeat

Interactive pieces:

- A target center is chosen.
- The player asks locals for clues.
- During daytime, the fugitive is placed into the village/town scene as an agent.
- Mission triggers watch whether the fugitive or player is defeated.
- Success/failure comes from scene outcome, not a menu branch.

Design takeaway:

The clue conversation points into a scene where the player must notice and confront a target. Dialogue is the lead-in, not the whole quest.

Companion translation:

- Klethi should identify an old contact in a tavern/town scene.
- Deshavi should track a pursuer or survivor into a village/town scene.
- Rolf's public-name challenge could place the heckler in a town scene or lord hall.

### Escort Merchant Caravan

Native reference:

- `module_dialogs.py`: `qst_escort_merchant_caravan`
- `pt_merchant_caravan`

Interactive pieces:

- A caravan party is spawned.
- The caravan can follow the player or wait.
- Completion happens near the target center.
- The caravan speaks differently before escort, during escort, and near destination.

Design takeaway:

An escort is interactive because the player has a moving object with simple orders. Even without scripted ambushes, the map object creates risk and pacing.

Companion translation:

- Ymira, Firentis, Deshavi, and Jeremus can all benefit from escortable refugee/wounded/supply parties.
- Borcha's road quest should almost certainly use a moving party or trail route.
- Baheshtur's rider oath could use a rider party that follows, waits, or bolts depending on treatment.

### Village Bandit Infestation

Native reference:

- `module_game_menus.py`: village menu detects `slot_village_infested_by_bandits`
- `mnu_village_infest_bandits_result`
- `mt_village_attack_bandits`

Interactive pieces:

- The village menu changes based on a village slot.
- Bandit and farmer visitors are placed in the village scene.
- Battle result drives success/failure.
- Village state, relation, and rewards change after the fight.

Design takeaway:

The world location itself should change when a quest is active. A village with a quest should expose different actions, scene visitors, and outcomes.

Companion translation:

- Firentis restitution villages should expose "leave guards," "speak to elder," and possibly "defend from reprisals."
- Deshavi trail villages should expose "inspect tracks," "hide vulnerable people," and "set ambush."
- Alayen's standard oath could expose a lord/village/town public witness action.

### Follow Spy / Meet Spy

Native reference:

- `module_dialogs.py`: `qst_follow_spy`, `qst_meet_spy_in_enemy_town`
- `pt_spy`
- `pt_spy_partners`
- town walker spy setup

Interactive pieces:

- A spy and handler are spawned as map parties.
- The spy travels to a meeting.
- The player must follow without disrupting the target.
- Capturing both, one, or neither produces different reward/failure outcomes.
- Meet-spy uses recognition details: worn item plus call-and-response phrases.

Design takeaway:

Native stealth quests use identity and observation, not only combat. Partial success is especially important: catching the handler but not the spy is different from catching neither.

Companion translation:

- Klethi's old-job quest should use a contact with a phrase, item, or tavern recognition clue.
- Deshavi's pursuer quest should use map tracking and ambush timing.
- Borcha's road quest can use suspicious parties that flee if approached wrong.

### Scout Waypoints

Native reference:

- `module_simple_triggers.py`: `qst_scout_waypoints`

Interactive pieces:

- Three waypoint parties/centers are selected.
- The player completes each by moving within range.
- Each visit displays feedback.
- The quest succeeds only after all targets are checked.

Design takeaway:

Map travel can be a quest verb. Not every quest needs a menu or mission if the travel itself is tracked.

Companion translation:

- Deshavi and Borcha should use tracked route points.
- Artimenner can inspect multiple siege weak points.
- Nizar can mark charge positions or retreat routes before battle.

### Duel For Lady / Named Lord Confrontations

Native reference:

- `module_dialogs.py`: `qst_duel_for_lady`
- `module_mission_templates.py`: duel result calls success/failure

Interactive pieces:

- The quest names a specific target lord.
- The player confronts him in dialogue.
- The confrontation transitions into a duel.
- Reward dialogue has multiple player tones.

Design takeaway:

Named NPC confrontation works when the target exists in the normal political world and the outcome is resolved physically or socially.

Companion translation:

- Rolf's name challenge should use a named public challenger.
- Alayen's standard quest should involve a lord/elder public witness, with possible duel or humiliation.
- Nizar's glory quest should have a named rival, scout, or enemy captain witness.

## Current Companion Quest Gap Audit

The companion system has improved substantially: pending incidents are party-guarded, witnesses exist, direct companion dialogue exists, camp fallbacks exist, and branch outcomes affect approval/quest state. The remaining problem is interactivity depth.

Current common weaknesses:

- Too many climaxes happen in one dialogue state or one camp menu.
- Witnesses describe the world but often do not create a world object.
- Few companion quests spawn parties, place agents in scenes, or modify map locations.
- Failure is usually "hard outcome selected," not "the player failed to protect, arrive, win, pay, track, or persuade."
- There are few timed pressures, travel checkpoints, partial successes, or cleanup risks.
- Companion presence is mostly checked by `main_party_has_troop`, not staged as a person standing in a scene with something to say.

New standard:

Every companion personal quest should have at least one interactive field surface beyond camp/direct talk. Dialogue may frame the issue, but the player should then do something in the world.

## Companion Quest Design Standard

Each companion quest should include these beats:

1. Trust Opening
   - Companion explains the personal wound/value.
   - Quest framework starts or unlocks the quest.

2. Field Trigger
   - A campaign event chooses a focus: center, party, troop, scene, item, or target amount.
   - The quest stores that focus in quest slots/globals and journal text.

3. Travel or Preparation
   - The player must go somewhere, wait, train, scout, escort, pay, gather supplies, inspect a scene, or speak to an external actor.

4. Interactive Climax
   - At least one of these must happen:
     - Scene fight or duel.
     - Spawned party escort/pursuit/ambush.
     - Timed pressure with interruption.
     - Named NPC confrontation.
     - Resource delivery/payment with real costs.
     - Multi-location scouting or inspection.

5. Branch Outcome
   - Good, hard, and bad outcomes should be produced by what happened, not only by menu choice.
   - Partial success should be allowed where appropriate.

6. Companion Aftermath
   - Companion reacts to facts: who lived, what was spent, what was hidden, what was witnessed.
   - Camp report and quest journal update.

7. Cleanup
   - Pending globals reset.
   - Spawned parties removed or released.
   - Scene visitors no longer appear.
   - Quest state and warning state are synchronized.

## Minimum Interactive Bar

A companion quest is not interactive enough if its field test can be summarized as:

"Talk to companion, click one of three options, receive approval/result."

A companion quest reaches the minimum bar if it has:

- A focus object: center, troop, party, item, or amount.
- A world action: travel, scene entry, escort, fight, trade, train, scout, or timed waiting.
- A witness who can react after the action.
- A failure or complication that can happen without the player choosing the "bad" dialogue option.

A companion quest reaches the ideal bar if it has:

- Two or more world actions.
- At least one optional shortcut or alternate route.
- Partial success.
- Persistent aftermath visible in reports, journal text, party morale, center relation, or future incidents.

## Native-Inspired Companion Redesign Targets

### Borcha - The Road Keeps Its Own

Native model: scout waypoints plus follow-spy.

Interactive design:

- Select three road/trail points near bandit or horde pressure.
- Borcha marks tracks after the player gets close enough.
- A suspicious rider/road party flees if approached directly.
- Outcomes:
  - Good: shadow the road party and expose a safer route.
  - Hard: ambush them early and take prisoners.
  - Bad: ignore signs or attack the wrong party, increasing road pressure.

### Marnid - The Honest Price

Native model: collect taxes plus merchant caravan.

Interactive design:

- A market contact or caravan carries disputed goods.
- Player can audit ledger, escort goods, pay fair restitution, or exploit shortage.
- Timed price pressure should rise if delayed.
- Outcomes:
  - Good: honest trade and stable relations.
  - Hard: hard bargain with visible resentment.
  - Bad: profiteering that creates future market distrust.

### Ymira - Mercy Under Arms

Native model: kidnapped girl plus escort caravan.

Interactive design:

- Captives/refugees become a small escortable party or a vulnerable group at a focus village.
- Slavers, raiders, or deserters can intercept if the party is left unguarded.
- Outcomes:
  - Good: escort and shelter vulnerable people.
  - Hard: ransom able-bodied captives to fund the weakest.
  - Bad: keep captives chained or sell them.

### Rolf - A Name Worth Wearing

Native model: duel for lady plus named lord confrontation.

Interactive design:

- A public challenger appears in town/lord hall.
- Player decides whether Rolf answers with service, ceremony, duel, or humiliation.
- Outcomes:
  - Good: public service proves the name.
  - Hard: duel or intimidation preserves dignity.
  - Bad: performative cruelty makes the name hollow.

### Baheshtur - The Unbroken Saddle

Native model: follow party plus ransom negotiation.

Interactive design:

- Beaten riders or Black Khergit scouts become a map party.
- Player can let them swear freely, escort them, pursue them, or force submission.
- Outcomes:
  - Good: freely sworn riders.
  - Hard: honorable pursuit and surrender.
  - Bad: forced submission, future resentment.

### Firentis - Debt of the Sword

Native model: village bandit infestation plus restitution delivery.

Interactive design:

- Focus village exposes actions: speak to elder, leave guard detachment, deliver supplies, defend from reprisal.
- Confession can happen in public, with villagers reacting.
- Outcomes:
  - Good: protection and restitution visibly aid the village.
  - Hard: truth and judgment without comfort.
  - Bad: silence or coercive "protection."

### Deshavi - Tracks Through Ash

Native model: scout waypoints plus hunt fugitive.

Interactive design:

- Player tracks survivor signs across village/town/caravan points.
- A pursuer or slaver party appears if the trail is followed.
- Outcomes:
  - Good: hide/shelter vulnerable survivors.
  - Hard: ambush pursuers.
  - Bad: reckless hunt that exposes survivors.

### Matheld - No Backward Step

Native model: train peasants plus village attack.

Interactive design:

- A line drill or shield-wall practice scene occurs after a hard battle.
- Player can train formation breathing, force a direct stand, or demand blood-price.
- A later skirmish tests whether the line learned discipline or appetite.
- Outcomes:
  - Good: courage that saves lives.
  - Hard: fierce stand with higher cost.
  - Bad: reputation bought with bodies.

### Alayen - The Standard and the Self

Native model: named lord confrontation plus scout waypoint/public witness.

Interactive design:

- A standard oath must be witnessed by elder/lord/troops at a focus location.
- Player chooses protection, prestige, or silence.
- Optional duel or public challenge if insulted.
- Outcomes:
  - Good: honor as obligation.
  - Hard: honor as obedience/prestige.
  - Bad: standard used as vanity.

### Bunduk - The Men Who Hold the Line

Native model: collect taxes plus company petition.

Interactive design:

- Rankers bring a petition over pay, watches, stores, or bad orders.
- Player can inspect watch bill, pay arrears, change stores, or crack down.
- If delayed, the grievance can escalate to desertion/mutiny pressure.
- Outcomes:
  - Good: practical repair.
  - Hard: partial compromise.
  - Bad: obedience first, warning later.

### Katrin - The Last Coin in Camp

Native model: collect taxes plus company accounts.

Interactive design:

- The ledger should produce a timed camp shortage: food, wages, medicine, arrears.
- Player can use accounts/ration menus as real levers.
- A troop/camp witness should report whether the policy is felt as fair.
- Outcomes:
  - Good: stores and arrears first.
  - Hard: fair rationing.
  - Bad: momentum bought with tomorrow's hunger.

### Jeremus - Hands That Will Not Harden

Native model: kidnapped girl plus scene casualty check.

Interactive design:

- After battle, a triage scene places wounded allies, enemies, prisoners, and followers in one place.
- Player can spend medicine, time, guards, or coin.
- Failure can occur if delayed after heavy casualties.
- Outcomes:
  - Good: need before banner.
  - Hard: hard triage.
  - Bad: company-first care that leaves moral injury.

### Nizar - The Impossible Charge

Native model: duel/confrontation plus scout waypoint.

Interactive design:

- Player marks charge lanes, dust screens, or retreat points before a battle.
- Charge can trigger a small encounter or battle setup.
- Outcomes:
  - Good: daring with a way out.
  - Hard: dazzling charge with risk.
  - Bad: spend blood for a legend.

### Lezalit - Discipline Without Chains

Native model: train peasants.

Interactive design:

- Captured Imperial drill notes become a practice field scene.
- Player watches a drill round or sparring exercise.
- Player can explain purpose, punish hesitation, or refuse the method.
- Outcomes:
  - Good: hard standards with meaning.
  - Hard: fear made orderly.
  - Bad: refusal or cruelty that leaves discipline unresolved.

### Artimenner - The Siege That Should Have Worked

Native model: scout waypoints plus siege scene setup.

Interactive design:

- Player inspects multiple siege weak points or construction sites.
- Artimenner identifies a flaw; the player chooses rebuild, improvisation, or denial.
- A later siege/construction check proves the choice.
- Outcomes:
  - Good: rebuild properly.
  - Hard: lean workaround.
  - Bad: deny fault and risk future disaster.

### Klethi - A Knife With a Name

Native model: meet spy in enemy town.

Interactive design:

- A tavern contact requires a phrase, item, or recognition tell.
- Player can let Klethi handle it, protect her openly, or use the secret for profit.
- Optional scene/tavern fight if the contact is crossed.
- Outcomes:
  - Good: Klethi chooses her own terms.
  - Hard: protected but exposed.
  - Bad: old secret weaponized.

## Implementation Pattern

For each companion, create or confirm:

- Quest metadata in `src/quests`.
- A companion opening dialogue.
- A field trigger script that chooses a focus object.
- A journal line that tells the player where to go or what to do.
- One world-facing surface:
  - `src/dialogs/ZC01_centers_and_economy`
  - `src/dialogs/ZC02_townsfolk_and_special_npcs`
  - `src/dialogs/ZD01_encounters_battles_and_prisoners`
  - `src/dialogs/ZZ99_misc_dialogs`
  - `src/menus/centers`
  - `src/menus/camp`
  - `src/mission_templates`
  - `src/triggers`
- Outcome scripts that apply approval, quest state, rewards, warnings, and world consequences.
- Cleanup through departed-companion and quest-failure paths.

## Companion Quest Acceptance Checklist

Before calling a companion quest "immersive," answer yes to these:

- Does the quest require the companion to be in the party at every trigger and resolution point?
- Does it choose and store a concrete focus object?
- Does the journal tell the player where to go or what to do?
- Does the player perform a world action beyond talking to the companion?
- Can something go wrong without choosing the obvious bad option?
- Does at least one non-companion witness react?
- Does the companion react after the external witness/action?
- Are good, hard, bad, and partial outcomes supported where appropriate?
- Are spawned parties/agents/focus globals cleaned up?
- Does the aftermath appear in reports, journal text, morale, center relation, party state, or future incidents?

## Priority Recommendations

Highest priority upgrades:

1. Ymira, Firentis, Deshavi: add escort/travel/focus-village actions.
2. Lezalit, Matheld: add training or formation mission scenes.
3. Katrin, Bunduk: add timed company-account pressure and escalation.
4. Klethi, Borcha: add spy/tracking/recognition mechanics.
5. Artimenner, Nizar: add setup points that affect later battle/siege outcomes.

This should be the bar going forward: companion quests should feel like native quests with companion personality layered on top, not companion conversations with quest labels attached.
