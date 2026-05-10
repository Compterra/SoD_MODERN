# PoP Quest Audit

## Purpose

This audit reviews how `References/PoP` structures quests, with special attention to patterns that can improve our companion quests. PoP's strongest quest work is not just extra dialog. It ties quests into campaign facts, map parties, battle outcomes, scene visits, timers, faction relationships, and long-tail progression systems.

Primary files reviewed:

- `References/PoP/Source/module_quests.py`
- `References/PoP/Source/module_dialogs.py`
- `References/PoP/Source/module_game_menus.py`
- `References/PoP/Source/module_scripts.py`
- `References/PoP/Source/module_simple_triggers.py`
- `References/PoP/Source/module_mission_templates.py`
- `References/PoP/Source/module_party_templates.py`
- `References/PoP/POP_Knighthood_and_Qualis_Analysis.md`
- `References/PoP/POP_Companion_Interactions.md`

## High-Level Findings

PoP makes quests feel larger than menu selections by letting quest state live in several systems at once:

- Quest targets are often selected from active campaign conditions, not hardcoded fiction.
- Quest parties and lairs exist on the campaign map and can be defeated, escaped, attached, or replaced.
- Battle victory menus resolve quest progress, rewards, partial credit, and failure states.
- Scene missions can update quest state during play, especially for investigation or supernatural quests.
- Quest notes are updated as stage-aware journals, not just static descriptions.
- Expiration and cooldown slots keep quest availability believable.
- Faction and order reputation gates make quest access feel earned.
- Long-tail rewards, such as Qualis Gem and knighthood systems, make quest outcomes matter beyond immediate cash.

The result is that PoP quests frequently feel like things happening inside the campaign world rather than conversations attached to NPCs.

## Quest Catalog Deltas

PoP keeps many native-style quests, then layers in custom quests and variants. Notable custom or heavily extended quests include:

- `qst_ghost_lady`
- `qst_marauding_jatu`
- `qst_order_bounty`
- `qst_order_tournament`
- `qst_order_challenge`
- `qst_order_grandmaster`
- `qst_order_rivalry`
- `qst_collect_men`
- `qst_destroy_bandit_lair`
- `qst_rescue_daughter`
- `qst_escort_peasants`
- `qst_track_down_bandits`
- `qst_track_down_provocateurs`
- `qst_retaliate_for_border_incident`
- `qst_raid_caravan_to_start_war`
- `qst_cause_provocation`
- `qst_old_tale_part_1`
- `qst_old_tale_part_2`
- `qst_horse_armor`

The most useful examples for companion quest design are `ghost_lady`, the order quest family, `destroy_bandit_lair`, `track_down_bandits`, `rescue_daughter`, and the Old Tale/Old Ruins progression chain.

## Core PoP Quest Patterns

### 1. Dynamic Quest Selection

Relevant source:

- `module_scripts.py`, `script_get_quest`
- `module_scripts.py`, `script_get_dynamic_quest`

PoP does not always choose quests by simple random selection. It asks the campaign for plausible targets:

- `track_down_bandits` can target parties that recently attacked travelers.
- `retaliate_for_border_incident` looks for hostile faction conditions and a suitable lord target.
- `destroy_bandit_lair` chooses a bandit lair or spawn point connected to the quest giver's region.
- `rescue_prisoner` and similar quests are gated by actual world state.

Design lesson: companion quests should begin from something real in the current campaign. If Borcha wants to find a raider trail, the target should be a real nearby bandit party or spawn area. If Firentis wants redemption, the hostage, village, or lord involved should exist in the world and have consequences.

### 2. Quest Timers, Cooldowns, and Retry Control

Relevant source:

- `module_simple_triggers.py`, daily quest timeout handling around the quest slot iteration

PoP uses quest slots for expiration, cooldown, and "do not give again yet" behavior. Order quests receive special success/fail/cancel handling, and quest notes are updated as deadlines change.

Observed slot behavior in decompiled source:

- State and stage values often use raw quest slots such as `11`.
- Expiration commonly appears around slot `23`.
- Cooldown or temporary unavailability commonly appears around slot `25`.
- Quest notes are refreshed when days remaining change.

Design lesson: companion quests need graceful expiry and re-entry. A companion should be able to say, "We missed the trail, but I heard another lead," rather than leaving broken quest state behind.

### 3. Battle Outcome Hooks

Relevant source:

- `module_game_menus.py`, `mnu_total_victory`

PoP resolves several quests inside the victory flow:

- `track_down_bandits` succeeds when the target party or attached target is defeated, with scaled rewards if allies helped.
- `retaliate_for_border_incident` succeeds when the specific target lord's party is defeated.
- `rescue_daughter` adds the rescued troop to the player's party after defeating the target.
- `order_bounty` awards progress based on defeated party template, faction, and attached parties.

Design lesson: companion quest progress should happen when the player does the thing, not only after reporting back. If a companion asked for justice against a specific band, the victory screen should acknowledge their presence and update the quest immediately.

### 4. Knighthood Order Quest Loop

Relevant source:

- `module_dialogs.py`, order hall and order quest dialog
- `module_game_menus.py`, order-related menus and victory checks
- `POP_Knighthood_and_Qualis_Analysis.md`

PoP's order system gives the player a recurring quest board with identity and progression:

- Joining an order can require a physical arena challenge against order troops.
- Order bounty quests score progress from enemy factions, party templates, and battle outcomes.
- Order tournaments direct the player to a town event.
- Order challenges require renown or restricted forms of force growth.
- Order rivalry quests target enemy order patrols.
- Relationship and cooldown values gate availability.

Design lesson: companion quest chains can borrow the "identity loop" without becoming menus. A companion can have a personal code, a public test, a rival faction, a reputation gate, and repeatable tasks that reinforce who they are.

### 5. Ghost Lady Investigation

Relevant source:

- `module_dialogs.py`, ghost lady dialog block
- `module_mission_templates.py`, ghost lady scene triggers
- `module_simple_triggers.py`, ghost lady auto-start/setup

The Ghost Lady quest is the strongest PoP model for immersive dialog-driven questing. It includes:

- An apparition or scene-based quest giver.
- A real investigation setup with suspects, a scribe, and a dead husband.
- Quest slots storing suspect identities, roles, and stage data.
- A bitmask-like clue state, where talking to suspects sets different bits.
- Quest notes that list suspects and update as the player gathers testimony.
- A final accusation, possible combat, reward, or failure.

Design lesson: companion quests should use staged investigation and scene dialog when the subject is personal. A Klethi, Ymira, Firentis, or Jeremus quest can become far more memorable if the player actually questions villagers, compares stories, and then chooses whom to confront.

### 6. Destroy Bandit Lair

Relevant source:

- `module_scripts.py`, dynamic lair target selection
- `module_game_menus.py`, lair battle success/failure handling

PoP's lair quest is useful because it joins map selection, scene combat, and cleanup:

- A quest giver points the player toward a plausible lair.
- The target exists as a real party/location.
- The scene battle result determines success or failure.
- The lair is removed or reset after completion.

Design lesson: companion quests involving revenge, rescue, scouting, or old enemies should often end in a specific scene battle, not a generic conversation.

### 7. Old Tale and Old Ruins Progression

Relevant source:

- `module_simple_triggers.py`, Old Tale and Old Ruins stage handling
- `POP_Knighthood_and_Qualis_Analysis.md`

PoP uses reading, delayed construction, and scene transformation to make long-form progression feel tangible:

- Reading an old diary advances `qst_old_tale_part_1`.
- A delayed trigger updates old ruins after the expected date.
- The site changes scene and the quest completes when the work is done.
- Long-tail rewards connect to deeper systems such as gems, strongholds, and order progression.

Design lesson: an engineer, scholar, healer, or noble companion quest can include visible world change. Artimenner restoring a bridge, Jeremus rebuilding an infirmary, or Ymira founding a refuge should use timers and altered locations.

### 8. Companion Presence Outside Companion Quests

Relevant source:

- `POP_Companion_Interactions.md`

PoP lets companions interrupt hostile encounters through generic response dialog. This gives party members a sense of presence even when the current quest is not "their" quest.

PoP also allows companions to be dispatched as trainers for custom knighthood orders. This creates a strategic tradeoff: the player may lose access to a companion temporarily in exchange for long-term troop improvement.

Design lesson: companion quest polish should include presence checks and party checks, but it should also create intentional absence. A companion being away training, researching, scouting, or negotiating should be a valid state with clear consequences and return timing.

## Lessons For Our Companion Quests

### Make Quest Starts Conditional On Presence

The original companion bug report was that some functions trigger when the companion is not in the party. PoP reinforces the fix: immersive companion quests should only use active companion dialog, interjections, and scene participation when the companion is actually present and available.

Every companion quest trigger should check:

- Companion is in the player's party.
- Companion is not wounded if the scene requires them to fight or travel.
- Companion is not currently dispatched, imprisoned, training, or otherwise unavailable.
- Companion is not separated by an active mission state.
- The quest is not on cooldown, expired, completed, or blocked by another active companion quest.

### Use Active World Targets

Companion quests should prefer live campaign entities:

- A real village recently raided.
- A bandit party near the companion's origin.
- A lord who actually holds a prisoner.
- A town where the companion has a relationship.
- A lair, hideout, bridge, ruin, shrine, or order hall that exists on the map.

This is the biggest difference between a quest that feels authored and a quest that feels like a menu.

### Move Progress Into World Events

Quest progress should update from:

- Battle victory menus.
- Scene triggers.
- Town/village menus.
- Dialog with multiple NPCs.
- Daily simple triggers.
- Party defeat or escape.
- Companion temporary absence and return.

Companion quests should not rely only on "talk to companion, choose option, receive reward."

### Use Investigations For Personal Stories

PoP's Ghost Lady structure is a strong fit for companion stories:

- Store suspect or witness troops in quest slots.
- Use a bitmask for which testimonies were collected.
- Update quest notes after each testimony.
- Let the companion react differently depending on the evidence.
- Allow wrong accusations, partial truth, mercy, duel, bribe, or public exposure outcomes.

This would suit Klethi, Firentis, Ymira, Jeremus, Deshavi, and Katrin especially well.

### Use Order-Style Loops For Martial Companions

PoP's order quests are a strong model for Lezalit, Matheld, Alayen, Rolf, Nizar, Baheshtur, and Bunduk:

- Public challenge in an arena or training ground.
- Bounty progress against a chosen enemy type.
- Rival patrol or champion encounter.
- Renown, relation, or troop-quality requirement.
- Repeatable but cooldown-gated tasks after the personal quest is complete.

The companion's values should define the loop. Lezalit wants discipline. Matheld wants proof in battle. Alayen wants honor. Rolf wants recognition. Bunduk wants justice for soldiers.

### Let Absence Matter

PoP's companion trainer concept is valuable because it turns a companion into a strategic asset outside the party.

Possible companion applications:

- Artimenner leaves to supervise construction.
- Jeremus stays in a village to treat an outbreak.
- Deshavi scouts ahead for several days and returns with map intelligence.
- Borcha infiltrates a caravan route and marks a bandit lair.
- Lezalit trains militia, improving a village defense outcome.
- Katrin organizes supplies, reducing party food consumption after success.

The key is that absence must be explicit, timed, journaled, and reversible.

## Companion Redesign Applications

### Borcha / Deshavi: Trail Quests

Use `track_down_bandits` as the model.

- Select a real bandit party, lair, or spawn point based on recent attacks.
- Companion comments at the initial trail site.
- Player can follow tracks through a village, road menu, or map marker.
- Battle victory resolves the target and companion reaction.
- Partial credit if an ally defeats the target first.

### Klethi: Witness And Suspect Quest

Use `ghost_lady` as the model.

- Choose a town/village with three witnesses and one guilty party.
- Track testimony with clue bits.
- Let the player accuse early, accuse correctly, accept a bribe, or let Klethi handle it.
- Wrong accusation damages companion trust or local relation.
- Correct accusation can become a duel, street fight, or stealth confrontation.

### Firentis: Redemption Rescue

Use `rescue_daughter` and `destroy_bandit_lair` as models.

- Select a real hostage, family member, or prisoner in a hostile party/lair.
- Firentis must be present for the confession and resolution.
- Battle victory adds the rescued NPC or changes village state.
- Mercy versus vengeance choices affect Firentis morale and honor.

### Lezalit / Matheld: Public Challenge

Use order challenge and arena join tests as models.

- Start at a castle, town arena, or training field.
- Fight a structured challenge with the companion watching or joining.
- Dialog before and after combat changes the meaning of victory.
- Failure should not hard-break the chain; it can add cooldown or a rematch path.

### Artimenner: Restoration Project

Use Old Tale and Old Ruins as the model.

- Discover a broken bridge, mine, tower, or ruin.
- Gather tools, workers, and protection.
- Artimenner leaves temporarily to supervise.
- A daily trigger completes construction after a fixed period.
- The location visibly changes or unlocks a new menu benefit.

### Jeremus / Ymira: Humanitarian Scene Quest

Use investigation plus timer patterns.

- Travel to a village with sickness, refugees, or a wounded notable.
- Gather herbs, supplies, testimony, or protection.
- A scene event can turn violent if the player threatens, delays, or accuses the wrong person.
- The companion's worldview should matter in the resolution.

### Bunduk / Katrin: Soldier And Supply Quests

Use order bounty scoring and progress notes.

- Track food, wages, veteran casualties, or militia training progress.
- Battle or escort outcomes increment a visible quest score.
- Success unlocks a practical party benefit, not just relation.

## Acceptance Checklist For Improved Companion Quests

A redesigned companion quest should pass these checks:

- The companion must be in the party before their quest starts.
- The companion must be present for key dialog, scene, and battle reactions.
- The quest uses at least one world target: party, center, lair, scene, lord, witness, or patrol.
- Progress can happen outside companion menus.
- Quest notes update after each meaningful stage.
- Failure, timeout, or target loss has a graceful path.
- Cooldown prevents immediate repetition or broken restarts.
- At least one stage uses a town, village, castle, lair, or battlefield scene.
- At least one choice changes a later dialog, fight, reward, or relationship outcome.
- The companion's personality determines the quest mechanics, not just the writing.

## Implementation Recommendations

For the next implementation slice, audit and rebuild one companion at a time. The best first candidates are:

1. **Klethi**: ideal for a Ghost Lady-style suspect investigation with clue bits and confrontation.
2. **Borcha or Deshavi**: ideal for dynamic party/lair tracking and battle result hooks.
3. **Firentis**: ideal for a rescue/redemption quest with real hostage and mercy choices.
4. **Artimenner**: ideal for a timed restoration project with visible world change.

The first companion rebuild should establish reusable helpers for:

- Companion availability checks.
- Companion quest stage/state slots.
- Clue bit tracking.
- Quest note refresh.
- Dynamic target selection.
- Companion scene visitor placement.
- Victory menu quest resolution.
- Expiration and cooldown handling.

Once those helpers exist, later companion quests can become much more interactive without duplicating fragile state logic.
