# Interactive Quest Bible

## Purpose

This document is the implementation bible for building interactive quest campaigns in this mod. It is written for IDE agents and future maintainers who need to create, audit, or upgrade quests without reducing them to camp menus and dialogue choices.

Use this as the standard for all companion quest work and for any major character-driven campaign quest.

Primary reference audits:

- `docs/Interactive_Quest_Design.md`
- `docs/PoP_Quest_Audit.md`
- `docs/108_Campaign_Quest_Audit.md`

Companion implementation roadmap:

- `docs/COMPANION_INTERACTIVE_QUEST_CHECKLIST.md`

Reference models:

- **Native Mount & Blade**: reliable quest lifecycle, concrete world targets, staged notes, spawned parties, scene outcomes, failure and cleanup.
- **PoP**: world-reactive targets, investigations, cooldowns, battle-result hooks, lairs, order loops, long-tail rewards.
- **108 Heroes**: hero campaigns, map-travel dialogue, in-battle dialogue, custom missions, result grades, companion progression, camp roles.

## Core Doctrine

A quest is not interactive because it has choices. A quest is interactive because the player changes the world, moves through the world, or risks losing something in the world.

Never ship a companion quest whose core experience is:

> Talk to companion, choose one of three answers, receive approval or reward.

A companion quest campaign should make the player:

- Travel somewhere with the companion.
- Meet or confront someone outside the party.
- Inspect, escort, protect, hunt, scout, train, negotiate, build, heal, or fight.
- See quest state update from world events, not only from dialogue.
- Hear the companion react while the event is happening.
- Receive a result shaped by action, timing, losses, witnesses, and choices.

## The Three-Layer Standard

Every interactive quest campaign should combine these three layers.

### 1. Native Structure

Native gives the minimum technical standard:

- Quest metadata exists.
- Quest slots store target center, troop, party, item, amount, state, giver, and timer.
- Quest notes update when the objective changes.
- Start, success, failure, cancellation, and cleanup are separate operations.
- Spawned parties and scene actors are cleaned up.
- Failure can happen through world events, not only dialogue.

### 2. PoP World Logic

PoP gives the campaign-reactive standard:

- Choose targets from live campaign state when possible.
- Use real parties, lairs, towns, villages, lords, witnesses, prisoners, patrols, and factions.
- Hook battle victory and mission results into quest progress.
- Use cooldowns and expiry so quests do not repeat or hang forever.
- Support partial success, target loss, and graceful retry paths.
- Use investigations, clue bits, suspect lists, and staged notes for personal mysteries.

### 3. 108 Presentation

108 gives the companion campaign standard:

- Treat a companion arc as a mini-campaign, not one quest menu.
- Use map-travel dialogue when the companion has something to say.
- Use in-scene or in-battle dialogue during the action.
- Build custom mission or scene episodes for personal moments.
- Grade outcomes beyond success/failure.
- Reward the companion directly with traits, roles, progression, or new abilities.
- Track multiple companion arcs in a readable summary.

## Mandatory Companion Availability Rule

The original bug class was companion functions triggering when the companion was not in the party. This must never return.

Before any companion quest trigger, line, menu, scene placement, map dialogue, battle interjection, reward, or consequence fires, check that the companion is available.

Minimum availability checks:

- Companion is in `p_main_party`.
- Companion is not disabled by a dispatched, training, scouting, construction, prisoner, separated, or temporary-away state.
- Companion is not wounded if the event requires combat or physical travel.
- Companion quest state allows this trigger.
- Another active scene/mission state is not already using the companion.
- The quest is not completed, expired, blocked, or cooling down.

If the companion is absent, the event should either:

- Not trigger.
- Queue a journal lead for later.
- Convert to a non-companion world event.
- Fail gracefully only if absence is an intended state.

Never let absent companions speak, appear in scenes, receive action credit, or resolve personal quest stages.

## Interactive Quest Anatomy

Every companion campaign should be built from episodes. Not every episode needs combat, but every episode needs a real world surface.

### Episode Beats

1. **Trigger**
   - Trust threshold, location, battle result, faction state, rumor, companion conflict, or campaign condition.

2. **Availability Gate**
   - Check companion presence and quest state before anything visible happens.

3. **Opening**
   - Companion speaks or a world witness introduces the lead.
   - Start or update the quest.

4. **World Target Selection**
   - Store a concrete focus object: center, party, troop, item, scene, faction, amount, route, lair, or witness set.

5. **Journal Update**
   - Tell the player where to go, whom to ask, what to protect, what to gather, or what to avoid.

6. **Travel Or Preparation**
   - The player moves, waits, trains, scouts, escorts, buys supplies, asks witnesses, follows tracks, or prepares a scene.

7. **Interactive Climax**
   - Scene confrontation, battle, duel, escort, ambush, investigation, construction, medical triage, stealth contact, or public hearing.

8. **Result Grade**
   - Resolve based on facts: survival, time, losses, evidence, target status, supplies spent, choice, companion health, witness reaction.

9. **Companion Aftermath**
   - Companion reacts to the facts and the player's approach.

10. **World Aftermath**
   - Apply center relation, party morale, companion trait, faction reaction, spawned party cleanup, role unlock, or future incident change.

11. **Cooldown Or Next Lead**
   - End cleanly, start cooldown, or update the campaign tracker with the next step.

## Minimum Interactive Bar

A quest meets the minimum bar only if it has all of these:

- A concrete world target.
- A world action beyond talking to the companion.
- A non-companion witness, enemy, victim, official, or location state.
- A failure or complication that can happen through play.
- A quest note update after each major stage.
- Cleanup for spawned parties, globals, scene visitors, and temporary slots.

A quest meets the ideal bar if it also has:

- Travel dialogue.
- In-scene or in-battle companion dialogue.
- Partial success.
- Result grading.
- Long-term companion unlock.
- Future reactivity from witnesses or affected locations.

## Approved Quest Verbs

Use these verbs when designing interactive quests. If the quest does not contain at least one of these verbs, it is probably too menu-heavy.

- **Travel**: visit a stored center, route, shrine, ruin, camp, bridge, village, castle, town, or battlefield.
- **Scout**: move near waypoints, inspect terrain, identify tracks, mark weak points.
- **Escort**: protect a moving party, refugee group, supply train, wounded troop, messenger, or witness.
- **Hunt**: find and defeat a real party, lair, fugitive, deserter, rival, or patrol.
- **Investigate**: question witnesses, compare statements, collect clue bits, identify suspect.
- **Confront**: challenge a named troop in a hall, tavern, village, arena, or street scene.
- **Duel**: resolve a public or private conflict with a controlled mission.
- **Train**: run practice bouts, drills, militia preparation, or formation tests.
- **Defend**: hold a village, camp, infirmary, bridge, convoy, or witness against attack.
- **Negotiate**: bargain with prisoners, elders, guilds, lords, bandits, debtors, or factions.
- **Deliver**: move supplies, medicine, ransom, tools, documents, weapons, or food.
- **Build**: inspect, gather, assign workers, wait for construction, defend work site, reveal changed location.
- **Heal**: triage wounded, gather medicine, choose priority, defend treatment site, track lives saved.
- **Infiltrate**: use phrase, disguise, contact, night scene, stealthy follow, or wrong-contact failure.
- **Judge**: accuse, pardon, expose, execute, compensate, or arbitrate with witnesses present.

## Required State Model

Every new interactive quest campaign should define its state model before implementation.

### Required Stored Values

Use existing project patterns when possible. Do not invent new globals if appropriate slots already exist.

Each campaign should store:

- Companion troop.
- Current campaign stage.
- Current episode stage.
- Target center.
- Target troop or witness.
- Target party.
- Target faction if relevant.
- Target item or required amount if relevant.
- Progress count.
- Required count.
- Deadline or expiration day.
- Cooldown day.
- Result grade.
- Failure reason.
- Clue bitmask if investigation.
- Temporary scene role markers if mission-based.
- Cleanup marker for spawned or borrowed objects.

### State Naming

Use readable constants for stages. Avoid magic values in new code.

Recommended stage categories:

- `inactive`
- `lead_available`
- `opening_pending`
- `active_travel`
- `active_investigation`
- `active_preparation`
- `active_scene`
- `active_battle`
- `waiting_for_return`
- `succeeded_poor`
- `succeeded_standard`
- `succeeded_ideal`
- `failed_recoverable`
- `failed_final`
- `cooldown`
- `completed`

### Result Grades

Do not use only pass/fail when the quest has meaningful nuance.

Recommended grades:

- `-1`: failed or abandoned.
- `0`: unresolved or no grade yet.
- `1`: completed with cost, doubt, or partial success.
- `2`: clean success.
- `3`: ideal success, unlocks extra reward or trait.

The grade should be based on observed facts, not just final dialogue choice.

## Journal Rules

The quest journal is part of the gameplay interface. Treat it as the player's memory.

Every major stage should update notes with:

- What happened.
- Where to go next.
- Who is involved.
- What is at risk.
- Whether a deadline exists.
- Whether the companion must be present.

For multi-companion systems, maintain a summary quest or report that shows:

- Each companion's current campaign state.
- Next actionable step.
- Completed arcs and unlocked roles.
- Waiting/cooldown states.
- Temporarily unavailable companions and return timing.

Do not leave stale notes pointing to removed parties, resolved witnesses, or expired leads.

## World Target Selection

Prefer live campaign targets over invented abstract targets.

Good target selection examples:

- Nearest village with recent raid or poor relation.
- Real bandit party near a companion's homeland.
- Actual prisoner held by a lord or center.
- Existing lair or spawn point in the region.
- Town where a witness or tavern contact can plausibly appear.
- Nearby castle/town scene if a custom scene does not exist yet.
- Faction patrol related to the companion's history.

Fallback targets are acceptable, but they must be stored and cleaned up.

If no plausible target exists:

- Delay the quest lead.
- Spawn a clearly quest-marked party.
- Use the nearest valid center.
- Convert to a rumor that waits for conditions.

Do not silently start an interactive quest without a valid target.

## Dialogue Rules

Dialogue should frame action, interrupt action, and interpret action. It should not replace action.

Use three layers of dialogue:

1. **Opening Dialogue**
   - Companion or witness introduces the problem.

2. **Field Dialogue**
   - Town, village, tavern, lair, battlefield, or travel dialogue gives clues and pressure.

3. **Aftermath Dialogue**
   - Companion reacts after the world outcome is known.

For companion dialogue:

- Check availability before every line.
- Use the companion's personality to change mechanics, not only flavor.
- Let other witnesses contradict or challenge the companion.
- Avoid repeating the same exposition in camp after the player already lived the event.

## Map-Travel Dialogue

Use map-travel dialogue for companion campaign beats that should feel spontaneous.

Good triggers:

- After winning a relevant battle.
- Near the companion's homeland or trauma site.
- After recruiting or dismissing a related companion.
- After entering a town with a stored lead.
- After failing or delaying a companion objective.
- After reaching a trust threshold.

Mandatory guardrails:

- Check companion availability.
- Add a cooldown so map dialogue is not noisy.
- Do not interrupt critical menus or mission transitions.
- If the player ignores it, store that it was offered.
- If the companion leaves before it fires, cancel or defer it.

## Mission And Scene Rules

Personal companion moments should use scenes whenever practical.

Scene setup should:

- Reset visitors.
- Place player, companion, witnesses, enemies, and civilians deliberately.
- Assign temporary mission roles.
- Preserve and restore normal troop state.
- Use staged mission progress variables or slots.
- Fire short dialogue beats during the action.
- Resolve success/failure from actual mission facts.

Scene examples:

- Town alley confrontation.
- Village elder hearing.
- Training field drill.
- Road ambush.
- Refugee escort arrival.
- Infirmary triage.
- Bridge or ruin inspection.
- Arena challenge.
- Lair rescue.

If a full custom scene is too expensive, reuse a town, village, tavern, training ground, castle hall, arena, or lair scene with controlled visitors.

## Battle And Victory Hooks

Battle should be able to advance companion campaigns.

Use victory hooks when:

- A target party is defeated.
- A specific troop is captured or killed.
- A companion survives or falls.
- A protected party survives.
- Enemy type progress should count.
- The player used allies and should receive partial credit.
- Captives or wounded should transfer after battle.

Use in-mission hooks when:

- A companion performs or witnesses an action.
- A duel or challenge result matters.
- A civilian, witness, or enemy is defeated.
- A wave, ambush, or timer reaches a threshold.
- A companion line should fire during the event.

Never resolve a companion battle objective without checking that the companion is present if their presence is narratively required.

## Failure, Timeout, And Recovery

Failure should be playable, not broken.

Supported failure modes:

- Deadline expired.
- Target party escaped or was destroyed by someone else.
- Companion absent at required moment.
- Witness killed.
- Protected party lost.
- Player defeated.
- Wrong accusation.
- Supplies spent elsewhere.
- Companion wounded.
- Player abandoned the quest.

Recovery options:

- Cooldown and new lead.
- Reduced reward.
- Partial success.
- Companion disappointment but arc continues.
- Alternate target.
- Public reputation loss.
- More difficult retry.

Use final failure sparingly, mostly for endings where the story genuinely closes.

## Cleanup Rules

Every quest implementation must have cleanup. This is not optional.

Cleanup should cover:

- Spawned parties.
- Temporary troops or prisoners.
- Visitor placement flags.
- Quest party slots.
- Scene role slots.
- Pending map dialogue globals.
- Companion temporary-away state.
- Target center slots.
- Target item or ransom state.
- Quest notes.
- Cooldowns and retry markers.

Cleanup must run for:

- Success.
- Failure.
- Cancellation.
- Companion departure.
- Companion death or disablement, if applicable.
- Quest timeout.
- Player defeat if the quest state depends on the mission.

## Companion Reward Rules

Reward the companion, not only the player.

Recommended rewards:

- Companion approval or trust.
- Companion personal trait.
- Companion title or status.
- Party skill bonus.
- Battle interjection unlock.
- Camp role.
- Training option.
- Construction/healing/scouting/logistics benefit.
- Unique item improvement.
- Relationship change with another companion.
- Center or faction relation tied to the companion's act.

Gold-only rewards are not enough for personal campaigns.

## Campaign Architecture For IDE Agents

When implementing a new companion campaign, use this workflow.

### Step 1: Audit Existing Companion State

Find:

- Companion troop id.
- Existing quest id.
- Existing companion approval/trust variables.
- Current triggers and menus.
- Current departure and cleanup logic.
- Existing helper scripts for party presence.

Do not duplicate helpers if the repo already has them.

### Step 2: Define Campaign Design

Write the campaign in this compact format before editing code:

```text
Companion:
Theme:
Opening trigger:
Required availability:
World target:
Travel/preparation action:
Scene or mission:
Battle/victory hook:
Witnesses:
Choices:
Failure modes:
Result grades:
Rewards:
Cleanup:
```

### Step 3: Add Or Update State Constants

Use named constants for:

- Stage.
- Result grade.
- Clue bits.
- Temporary scene roles.
- Cooldown state.

Avoid raw values in new campaign logic.

### Step 4: Implement Availability Gate First

Before adding content, add the guard script or checks that prevent absent companion triggers.

Recommended helper shape:

```text
cf_companion_campaign_available(companion, required_mode)
```

Modes can include:

- `dialog`
- `travel`
- `scene`
- `battle`
- `away_allowed`

Project implementation:

- Use `script_cf_sod_companion_campaign_available` for module-system gates.
- Pass one of `sod_companion_campaign_mode_dialog`, `sod_companion_campaign_mode_travel`, `sod_companion_campaign_mode_scene`, `sod_companion_campaign_mode_battle`, or `sod_companion_campaign_mode_away_allowed`.
- The current guard blocks invalid companion ids, non-companion troops, absent companions, resolved personal arcs, and wounded companions for scene or battle beats.
- Future temporary-away systems should extend this helper instead of adding scattered companion-presence checks.

### Step 5: Implement World Target Selection

Create or reuse a helper that selects and stores the target. It should return failure if no valid target exists.

The journal should not start the field stage until the target is valid.

### Step 6: Implement World Surface

Add at least one of:

- Center menu option.
- Town/village/tavern dialogue.
- Spawned party.
- Mission template.
- Scene visitor setup.
- Battle victory hook.
- Simple trigger for timer/progress.

### Step 7: Implement Result And Cleanup

Before adding polish, make sure success, failure, cancellation, and companion departure end cleanly.

### Step 8: Add Presentation Polish

Add:

- Companion field dialogue.
- Witness response.
- In-scene or in-battle short lines.
- Updated quest notes.
- Result grade messaging.
- Companion aftermath.

### Step 9: Verify

Run the relevant static/build checks used by the repo. For docs-only changes, no build is required. For code changes, use the established build and doctor commands.

## IDE Agent Acceptance Checklist

Do not call a companion campaign complete unless every item below is true.

- Companion cannot trigger or speak while absent.
- Quest has a stored world target.
- Player performs a world action beyond companion dialogue.
- Quest journal updates at each major stage.
- At least one external witness, enemy, victim, or location reacts.
- At least one failure or complication can occur through gameplay.
- Battle, scene, timer, or map progress can update the quest.
- Result grade is based on actual facts.
- Companion receives a meaningful personal outcome.
- Spawned objects and temporary state are cleaned up.
- Companion departure does not leave broken pending state.
- Quest can be delayed, failed, or retried without corrupting the campaign.

## Anti-Patterns

Avoid these:

- Companion quest resolved entirely in camp.
- Companion dialogue offered when companion is absent.
- One global variable controlling several companions without clear ownership.
- Quest notes that never update after start.
- Stages represented by unexplained magic numbers.
- Spawned parties with no cleanup path.
- Forced success after a battle where the companion was not present.
- Failure that only exists as a dialogue option.
- Rewards that are only gold or XP.
- Witnesses who only describe events but do not affect state.
- Menus that offer choices without travel, risk, cost, or consequence.

## Companion Campaign Templates

### Investigation Template

Best for Klethi, Firentis, Ymira, Jeremus, Katrin.

Required systems:

- Target center.
- Three or more witnesses.
- Clue bitmask.
- Accusation stage.
- Wrong accusation consequence.
- Companion reaction by evidence quality.
- Optional combat or public exposure.

Minimum stages:

1. Companion raises suspicion.
2. Player travels to target center.
3. Player questions witnesses.
4. Clue bits unlock final suspect.
5. Player accuses or delays.
6. Scene/dialogue/fight resolves.
7. Companion and center react.

### Tracking Template

Best for Borcha, Deshavi, Baheshtur, Nizar.

Required systems:

- Route or waypoint list.
- Target party or lair.
- Proximity checks.
- Ambush or pursuit.
- Battle result hook.
- Partial success if target escapes or allies intervene.

Minimum stages:

1. Companion identifies trail.
2. Player scouts two or three locations.
3. Target party appears or is identified.
4. Player shadows, ambushes, negotiates, or attacks.
5. Victory/escape updates quest.
6. Companion interprets outcome.

### Public Challenge Template

Best for Lezalit, Matheld, Alayen, Rolf, Bunduk.

Required systems:

- Named challenger or public witness.
- Arena, training field, castle hall, or village scene.
- Duel, drill, speech, or formation test.
- Result grade from performance.
- Reputation or companion trait outcome.

Minimum stages:

1. Insult, challenge, or dispute appears.
2. Companion asks to answer it.
3. Player selects public approach.
4. Scene challenge occurs.
5. Result is graded.
6. Witness and companion react.

### Humanitarian Template

Best for Jeremus, Ymira, Firentis, Katrin.

Required systems:

- Vulnerable group.
- Supplies, medicine, ransom, guards, or time cost.
- Escort, triage, or defense scene.
- Lives saved or lost.
- Moral aftermath.

Minimum stages:

1. Companion notices suffering.
2. Player identifies target center/group.
3. Player gathers resources or guards.
4. Scene or escort tests commitment.
5. Result grade counts saved/lost/cost.
6. Companion receives role or trust change.

### Construction Template

Best for Artimenner, Jeremus, Lezalit, Katrin.

Required systems:

- Target location.
- Material or labor requirements.
- Companion temporary assignment.
- Timer.
- Defense or inspection event.
- Visible or menu-level location change.

Minimum stages:

1. Companion identifies a fixable site.
2. Player inspects and commits resources.
3. Companion supervises work.
4. Timer advances.
5. Complication or defense event can occur.
6. Location changes or unlocks benefit.

## First Vertical Slice Recommendation

Build one companion campaign end to end before broad rewrites.

Recommended first candidate: **Klethi**.

Why:

- Investigation tests clue bits.
- Town/tavern scene tests external witnesses.
- Map-travel dialogue tests companion presence gates.
- Optional street fight tests mission/scene resolution.
- Result grading tests aftermath.
- Cleanup requirements are clear.

Second candidate: **Firentis**.

Why:

- Moral choices and result grades fit naturally.
- Village focus creates strong world state.
- Rescue/protection hooks test battle and witness reactions.

Third candidate: **Artimenner**.

Why:

- Construction tests timed absence and visible long-term payoff.

## Final Rule

If the player did not go somewhere, risk something, learn something from the world, or change something outside the companion menu, the quest is not done.
