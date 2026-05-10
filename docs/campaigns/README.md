# Campaign Framework

> Status: **target-state** design and content bible for future module-system implementation.  
> This document is intentionally written for later lowering into the Mount & Blade 1.011 module system, not as proof of a current runtime campaign engine.

## Purpose

This repo does not yet have a true campaign layer in the classic Mount & Blade sense.  
This document defines one for future use:

- campaigns are larger than quests
- campaigns contain branching storylines, player choice, and multiple endings
- campaigns can be short, medium, or long
- campaigns can unlock other campaigns
- side campaigns can temporarily replace the active campaign
- campaign outcomes should persist and reshape later content

The goal is to make the game feel like it has campaign arcs even though M&B 1.011 does not provide a native campaign system.

## How campaigns relate to the existing quest framework

Campaigns should be treated as the layer above quests.

- **Quests** are the executable units: tasks, offers, reactions, events, consequences.
- **Campaigns** are the narrative containers: a chain of related quests and branch points.
- **Campaign choices** decide which quests appear, which companion reactions matter, and which endings remain possible.
- **Campaign state** should be lowered into the same modular build pipeline later, but it should not be authored as a pile of unrelated quests.

In practical terms, a campaign can be made from:

- quest chains
- quest offers
- branch gates
- companion approval checks
- faction memory checks
- diplomacy checks
- world-state checks
- finale resolution states

## Core campaign design goals

1. **Branching matters**  
   The player should be able to make choices that redirect the campaign, not just change a reward line.

2. **Multiple endings matter**  
   Every campaign should have at least three meaningful resolutions where possible.

3. **Short and long campaigns both exist**  
   Some campaigns are one or two quest arcs. Others are multi-act storylines.

4. **Side campaigns can change the active campaign**  
   A side campaign may suspend, reshape, or replace the current campaign.

5. **Campaigns unlock campaigns**  
   Finishing one campaign can open another, or open a special branch of another campaign.

6. **Companion reactions should matter**  
   Campfire companions should react to campaign choices, not just isolated quest actions.

7. **The world should remember**  
   Campaign outcomes should affect diplomacy, faction memory, companion trust, market states, patrol pressure, and future offer availability.

## Recommended campaign hierarchy

Use this hierarchy when planning or documenting campaigns:

- **Campaign**
  - top-level story arc
  - owns the opening premise and final outcome
- **Act**
  - a major phase in the campaign
  - usually introduces a new conflict or pressure
- **Chapter**
  - a quest cluster or branch segment
  - usually resolves one obstacle
- **Branch**
  - a mutually exclusive or conditional route
- **Beat**
  - a specific event, conversation, or outcome
- **Ending**
  - the final state of the campaign

Not every campaign needs all of these as separate authored files.  
For short campaigns, an act and chapter can be the same thing.  
For long campaigns, each act may contain several chapters.

## Recommended campaign record format

Use this structure when authoring a campaign in docs.

```md
# Campaign ID

## Overview
- Title:
- Length:
- Type:
- Active or side campaign:
- Summary:

## Entry
- Unlock requirements:
- Starting conditions:
- Required world state:
- Required companion states:
- Required faction states:

## Core choices
- Choice 1:
- Choice 2:
- Choice 3:

## Branches
- Branch A:
- Branch B:
- Hidden branch:
- Failure branch:

## Campaign switches
- What campaign stays active:
- What campaign becomes active:
- What gets suspended:
- What gets unlocked:

## Endings
- Ending 1:
- Ending 2:
- Ending 3:
- Secret ending:

## World effects
- Companion effects:
- Faction effects:
- Diplomacy effects:
- Economy effects:
- Map pressure effects:

## Notes for later module implementation
- Quest chain mapping:
- Menu entry points:
- Trigger hooks:
- State storage:
```

This format is deliberately simple enough to lower later into quest chains, state slots, triggers, and menu text.

## Campaign state model

A campaign should have a small set of state types.

### 1. Active campaign

The main story the player is currently pushing forward.

### 2. Side campaign

A side campaign is a parallel arc that can:

- run alongside the active campaign
- temporarily take control of the player’s focus
- alter the active campaign’s next chapter
- unlock an alternate ending
- add or remove campaign flags

### 3. Suspended campaign

A campaign that remains alive in the background while another campaign takes the foreground.

Useful when:

- a political crisis interrupts a personal campaign
- a faction crisis becomes the new focus
- a companion quest chain needs to override the current main arc

### 4. Converged campaign

A campaign that merges back into the main arc after a side arc or detour.

### 5. Terminated campaign

A campaign that ends due to victory, failure, exile, betrayal, or forced abandonment.

## Branching rules

Campaign branches should follow these rules:

- every branch must be readable before the player commits
- player choice should create a real state change
- branches should be allowed to rejoin later, but not always
- a branch may unlock a different campaign rather than a different ending
- hidden branches should exist, but they should be discoverable through play
- a campaign should never require the player to guess an invisible rule without some earlier clue

## Ending types

Campaign endings should not all feel the same.  
Use distinct resolution types so the player feels the consequences.

Recommended ending categories:

- **victory ending** — the campaign succeeds cleanly
- **pyrrhic victory** — success with severe losses
- **compromise ending** — the player avoids the worst outcome but does not fully win
- **betrayal ending** — the campaign is twisted by a major choice
- **exile ending** — the player survives but loses the campaign’s core prize
- **collapse ending** — the campaign fails outright
- **redemption ending** — a character or faction is restored through difficult choice
- **domination ending** — the player seizes control of the campaign’s central force
- **secret ending** — only available through unusual choices or hidden conditions

## Campaign triggers and state sources

Campaigns should draw from the same kinds of state already used elsewhere in the framework:

- quest completion and failure
- offer acceptance and rejection
- companion approval and warning states
- diplomacy and treaty status
- faction hostility or memory
- world threat pressure
- player reputation and honor-like values
- party strength and losses
- village, caravan, and town outcomes
- special flags from prior campaign choices

This keeps campaigns compatible with the module system later and avoids inventing a disconnected narrative layer.

## Recommended authoring pattern

When writing a campaign proposal, use this order:

1. define the campaign premise
2. define the central conflict
3. define the player’s first meaningful choice
4. define the first branch split
5. define the second branch split or convergence
6. define the ending states
7. define what the campaign unlocks next

That sequence keeps a campaign from becoming a set of disconnected quest ideas.

## Suggested campaign file organization

For this repo, the most maintainable doc structure is:

- `docs/campaigns/README.md` — framework overview and authoring standard
- `docs/campaigns/campaign_catalog.md` — active campaign pitches and unlock table
- `docs/campaigns/campaign_branching_examples.md` — branch shapes and choice patterns
- `docs/campaigns/campaign_state_model.md` — persistent state, unlocks, and switching rules
- `docs/campaigns/campaign_content_examples.md` — fully written sample campaigns

This keeps the campaign layer separate from the quest framework docs while still staying close to the module-system workflow.

## Starter campaign catalog

The following are authored campaign pitches meant for later implementation.  
They are not current code claims.

### 1. The Road to the Crown

**Type:** main campaign  
**Length:** long  
**Role:** central political campaign

Premise:

The player rises from local contract work into a contest over legitimacy, territory, and the right to lead a coalition.

Main branches:

- lawful rise through noble recognition
- mercenary rise through contracts and leverage
- conquest rise through hard victories and fear
- hybrid rise through diplomacy and selective brutality

Possible endings:

- crowned and recognized
- crowned but hated
- power shared through coalition
- claimed by force and resisted
- abandoned after internal fracture

Unlocks:

- ruler campaigns
- faction governance content
- noble reconciliation arcs
- endgame coalition or empire campaigns

Campaign effect:

This campaign should be the structural bridge from “wandering warband” to “state actor.”

---

### 2. Ashes of the Steppe

**Type:** side campaign  
**Length:** medium  
**Role:** Black Khergit pressure arc

Premise:

The steppe corridor becomes unstable, and the player must decide whether to exploit, suppress, or redirect the pressure.

Main branches:

- destroy the warband route
- co-opt the route for profit
- redirect the pressure toward a rival
- negotiate a temporary corridor peace

Possible endings:

- route destroyed
- route converted into an asset
- route diverted but not ended
- the player becomes entangled with the warband

Unlocks:

- steppe-related raids
- scout and pathfinder bonuses
- Black Khergit pressure reductions or escalations
- future caravan and ambush campaigns

Campaign effect:

This campaign should change the active pressure on the world map rather than merely award loot.

---

### 3. Chains in the Market

**Type:** side campaign  
**Length:** short to medium  
**Role:** anti-slaver or slaver-linked choice arc

Premise:

A market, broker, or route tied to captivity becomes a political and moral test.

Main branches:

- destroy the chain
- regulate the chain
- exploit the chain
- rescue people and trigger retaliation

Possible endings:

- slavery network broken
- slavery network pushed underground
- player profits but loses moral allies
- freed people become a new support base

Unlocks:

- anti-slaver decree follow-ups
- Jotnar or mercy-aligned support
- underworld retaliation
- rescue campaigns

Campaign effect:

This campaign should directly alter faction memory and future market safety.

---

### 4. The Quiet Knife

**Type:** short side campaign  
**Length:** short  
**Role:** stealth, intrigue, and opportunism arc

Premise:

A small set of decisions with a large political effect.

Main branches:

- expose a secret
- steal a secret
- bury a secret
- sell a secret to a rival

Possible endings:

- secret exposed cleanly
- secret becomes leverage
- secret is buried but remembered
- secret is weaponized by another faction

Unlocks:

- espionage lines
- hidden companion reactions
- blackmail or diplomacy branches
- later intrigue campaigns

Campaign effect:

This campaign should feel small in duration but large in consequence.

---

### 5. The Last Banner of the East

**Type:** long campaign  
**Length:** long  
**Role:** endgame war campaign

Premise:

A large eastern force or coalition crisis forces the player to choose between defense, sacrifice, or aggressive counteroffensive.

Main branches:

- hold the line
- bait the enemy into overextension
- betray a rival to save the realm
- build a coalition through pressure and fear

Possible endings:

- defensive victory
- costly withdrawal
- coalition survival
- regional collapse
- the player becomes the dominant power

Unlocks:

- endgame campaign resolution
- postwar settlement campaigns
- late-game diplomacy
- successor campaigns for surviving factions

Campaign effect:

This should be the “big war” campaign for late-game play.

---

### 6. Mercy Under Chains

**Type:** companion-linked side campaign  
**Length:** short  
**Role:** moral choice arc

Premise:

A captivity event or rescue chain tests whether the player chooses mercy, efficiency, or cruelty.

Main branches:

- save captives at cost
- trade captives for advantage
- ignore the crisis
- exploit the crisis

Possible endings:

- trust and loyalty increase
- practical compromise
- moral rupture
- companion departure or warning

Unlocks:

- companion loyalty content
- rescue arcs
- anti-cruelty branches
- healer or conscience-related outcomes

Campaign effect:

This should be the bridge between companion depth and larger campaign design.

## Side campaigns that change the active campaign

This is a core feature worth supporting explicitly.

A side campaign should be able to do one of the following:

- **interrupt** the active campaign temporarily
- **overlay** a new urgent objective while the main campaign stays valid
- **replace** the active campaign if the choice is severe enough
- **split** the active campaign into two mutually exclusive tracks
- **merge** back into the original campaign after a decisive outcome

### Recommended switch types

- `suspend_and_replace`
- `overlay_and_return`
- `split_to_branch`
- `merge_back`
- `unlock_new_active`
- `terminate_old_and_start_new`

These are design terms for the docs. They can be lowered into module-system state later.

## Companion and faction integration

Campaigns should not live in isolation.

They should use:

- companion approval tiers
- companion warning confrontations
- companion personal quest gates
- faction memory and diplomacy
- ruler legitimacy and fear
- market and patrol pressure
- special regional threats

This is where campaigns become more than quest chains.  
They become a way to make the world react as a system.

## Recommended documentation split

If this campaign framework is expanded, the best structure is:

- **framework** — how campaigns work
- **catalog** — which campaigns exist
- **examples** — how choices branch
- **state model** — what persists
- **implementation notes** — how to lower the design into the module system later

That separation keeps the docs readable and makes it easier to move from design to implementation.

## Immediate next authoring targets

If this system is adopted, the next campaign docs to write should be:

1. `campaign_catalog.md`
2. `campaign_branching_examples.md`
3. `campaign_state_model.md`
4. one fully authored main campaign
5. one fully authored side campaign
6. one companion-linked campaign

## Module-system lowering notes

When this is implemented later, a campaign will likely lower into:

- quest chains
- chapter or stage transitions
- offer conditions
- companion approval checks
- world-state flags
- menu entry points
- trigger-driven switch logic
- ending resolution storage

That is the intended bridge from the doc design to the module system.

## Summary

Campaigns are the missing macro layer.

- quests are the playable tasks
- campaigns are the long-form story structures
- branches create choice
- endings create consequence
- side campaigns reshape the active story
- unlocks make the world feel persistent

That is the system this repo should author now so it can be implemented later without inventing it from scratch.
