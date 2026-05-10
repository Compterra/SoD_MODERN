# Campaign Content Examples

> Status: **target-state** examples only.  
> These are authored samples for future module-system implementation, not proof of a current runtime campaign engine.

## Purpose

This page turns the campaign format into usable examples.

It shows how to write:

- a main campaign
- a side campaign
- a companion-linked campaign
- branch outcomes
- campaign switches
- unlocks
- endings

The goal is to make the campaign layer feel concrete enough that later implementation can lower it into quests, flags, and menu logic without redesigning the narrative structure.

---

## Example 1: The Road to the Crown

### Overview

- **Campaign ID:** `campaign_road_to_the_crown`
- **Type:** main campaign
- **Length:** long
- **Role:** central rise-to-power arc
- **Active or side campaign:** active campaign
- **Summary:** The player rises from contract work into a contest over legitimacy, territory, and the right to lead a coalition.

### Entry

- The player has completed at least one major regional contract or conflict.
- The player has enough reputation to matter politically.
- At least one faction recognizes the player as relevant or dangerous.
- Companion approval is mixed or better.
- The world contains at least one active political pressure.

### Core choices

1. **Legitimacy route**  
   Seek noble recognition, marriage leverage, or formal vassalage.

2. **Mercenary route**  
   Build power through contracts, payment, selective aid, and leverage.

3. **Conquest route**  
   Seize strength through decisive victories, fear, and hard control.

4. **Coalition route**  
   Attempt to unite incompatible forces with diplomacy and conditional trust.

### Branches

#### Branch A — Lawful rise
The player pursues recognition and tries to become a lawful power.

#### Branch B — Mercenary rise
The player remains flexible and sells force where it is most useful.

#### Branch C — Conquest rise
The player builds a feared military base and coerces the world into acknowledging reality.

#### Branch D — Coalition rise
The player tries to stitch together allies, mercenaries, and fractured nobility.

#### Hidden branch — Regime maker
If the player combines legitimacy, fear, and coalition support in the right balance, the campaign can pivot into a more stable regime-ending than any single public branch predicts.

#### Failure branch — Fractured claim
If companions leave, diplomacy collapses, and too many factions oppose the player, the campaign can fail into exile or fragmentation.

### Endings

- **Recognized ruler** — the player gains stable authority and broad acknowledgment.
- **Feared ruler** — the player rules through intimidation and hard security.
- **Coalition ruler** — the player governs through a coalition with compromises.
- **False crown** — the player gains power but cannot stabilize it.
- **Exile claimant** — the player survives but loses the core political prize.
- **Collapse** — the campaign fails into disunity or betrayal.

### Unlocks

- ruler campaigns
- governance-focused campaigns
- noble reconciliation arcs
- post-campaign settlement arcs
- endgame coalition or empire campaigns

### World effects

- Companion approval shifts based on chosen route.
- Faction memory changes depending on legitimacy or conquest.
- Trade and patrol pressure shift after the final act.
- Campaign end state should feed later diplomacy and ruler content.

### Implementation notes

- Map each branch to a quest chain or campaign chapter chain.
- Use diplomacy, legitimacy, fear, and companion approval as major gate checks.
- Use faction memory and treaty outcomes as branch persistence.
- Use the ending state to unlock the next active campaign.

---

## Example 2: Chains in the Market

### Overview

- **Campaign ID:** `campaign_chains_in_the_market`
- **Type:** side campaign
- **Length:** short to medium
- **Role:** anti-slaver / slaver-linked moral pressure arc
- **Active or side campaign:** side campaign
- **Summary:** A market, broker, route, or prisoner network tied to captivity becomes a test of power and conscience.

### Entry

- The Slaver market or a captivity network is active in the world state.
- The player has a way to interact with trade, prisoners, or rescue opportunities.
- At least one companion with a strong moral stance is present or potentially relevant.
- A campaign or side quest is already using captivity pressure.

### Core choices

1. **Destroy the chain**  
   Break the network and accept retaliation.

2. **Regulate the chain**  
   Keep the network in a controlled but morally compromised form.

3. **Exploit the chain**  
   Use the network for money, manpower, or leverage.

4. **Rescue the captives**  
   Prioritize people over profit and trigger hostile reaction.

### Branches

#### Branch A — Purist break
The player commits to shutting the network down.

#### Branch B — Controlled compromise
The player keeps the network alive but tries to reduce harm.

#### Branch C — Exploitative profit
The player uses the network as a political or financial asset.

#### Branch D — Rescue pressure
The player centers the rescue outcome and absorbs the consequences.

#### Hidden branch — Replaced market
The player can convert a collapsed chain into a new support structure for allies or refugees.

#### Failure branch — Retaliation spiral
If the player half-commits and then fails to protect the aftermath, the network reasserts itself.

### Endings

- **Chain broken**
- **Chain regulated**
- **Chain exploited**
- **Captives freed**
- **Retaliation spiral**
- **Moral rupture** — companion trust is damaged or lost
- **Support network ending** — rescued people become a lasting factional asset

### Unlocks

- anti-slaver decree follow-ups
- Jotnar-aligned support
- mercy-focused companion content
- underworld retaliation
- rescue campaigns

### World effects

- Slaver pressure rises or falls depending on the chosen branch.
- Companion approval changes sharply for mercy-sensitive characters.
- Future prisoner or market offers should be altered by the campaign result.
- Jotnar or anti-slaver support should react to the outcome.

### Implementation notes

- This campaign should directly modify faction memory and market safety.
- It should trigger companion approval changes, especially Ymira, Jeremus, Katrin, and Firentis.
- It should be able to suspend or redirect other campaign arcs that depend on prisoner state.

---

## Example 3: Mercy Under Chains

### Overview

- **Campaign ID:** `campaign_mercy_under_chains`
- **Type:** companion-linked side campaign
- **Length:** short
- **Role:** moral choice arc and loyalty test
- **Active or side campaign:** side campaign
- **Summary:** A captivity event or rescue chain tests whether the player chooses mercy, efficiency, or cruelty.

### Entry

- A companion or captive crisis exists.
- At least one mercy-sensitive companion is present or reachable.
- The player has a real tradeoff instead of a free win.
- The campaign should be able to appear during travel, camp, or after a battle.

### Core choices

1. **Save captives at cost**
2. **Trade captives for advantage**
3. **Ignore the crisis**
4. **Exploit the crisis**

### Branches

#### Branch A — Compassion route
The player protects lives even when it costs resources.

#### Branch B — Pragmatic route
The player saves some lives but accepts an ugly compromise.

#### Branch C — Abandonment route
The player chooses not to intervene.

#### Branch D — Exploitative route
The player turns the situation into power.

#### Hidden branch — Quiet rescue
If the player has enough stealth, timing, or outside support, they can produce a lower-cost rescue.

#### Failure branch — Companion fracture
If the player repeatedly chooses cruelty, the companion arc can break instead of resolving.

### Endings

- **Trust ending**
- **Compromise ending**
- **Rupture ending**
- **Warning ending**
- **Companion departure warning**
- **Quiet rescue ending**

### Unlocks

- companion loyalty content
- rescue arcs
- anti-cruelty branches
- healer or conscience-related outcomes
- alternate campfire scenes

### Companion reactions

- **Ymira:** strongly favors rescue and mercy.
- **Jeremus:** favors careful rescue and humane compromise.
- **Firentis:** may accept hard necessity, but not exploitation.
- **Bunduk:** cares about whether the choice wastes the lives of ordinary soldiers.

### World effects

- Companion approval tiers should change immediately.
- Follow-up campfire dialogue should reflect the branch.
- Rescue success can unlock later moral or healer content.
- Cruel choices should create warning and rupture pressure.

### Implementation notes

- This campaign should bridge companion depth and campaign design.
- It should strongly affect Ymira, Jeremus, Firentis, and Bunduk.
- It should be able to suspend a larger campaign if the moral crisis becomes urgent enough.

---

## Example 4: The Quiet Knife

### Overview

- **Campaign ID:** `campaign_the_quiet_knife`
- **Type:** short side campaign
- **Length:** short
- **Role:** intrigue, secrecy, and opportunism arc
- **Active or side campaign:** side campaign
- **Summary:** A small set of decisions causes a disproportionate political effect.

### Entry

- A secret exists, or can plausibly be created.
- The player has access to one of the following:
  - a court
  - a camp
  - an informant
  - a spy-like contact
  - a rival power
- The player has at least one route to pressure or concealment.

### Core choices

1. **Expose the secret**
2. **Steal the secret**
3. **Bury the secret**
4. **Sell the secret**

### Branches

#### Branch A — Public exposure
The secret becomes visible to the world.

#### Branch B — Private leverage
The secret is retained as a bargaining tool.

#### Branch C — Buried but remembered
The secret disappears from public view but leaves a memory trace.

#### Branch D — Weaponized secret
The secret is sold or handed to a rival faction.

#### Hidden branch — Counterintelligence
The player discovers that the secret was bait and turns the operation back on the source.

#### Failure branch — Compromised
If the player is discovered too early, the entire campaign becomes defensive.

### Endings

- **Truth exposed**
- **Leverage secured**
- **Secret buried**
- **Secret weaponized**
- **Counterintelligence win**
- **Compromised ending**

### Unlocks

- espionage-related lines
- hidden companion reactions
- blackmail or diplomacy branches
- later intrigue campaigns
- secret-faction pressure hooks

### World effects

- Diplomatic trust changes depending on exposure or concealment.
- Companion reactions should vary based on whether the secret was used morally or opportunistically.
- Rival factions may gain warning or leverage from the outcome.

### Implementation notes

- This campaign should be fast and compact, but its outcomes should ripple into diplomacy and companion trust.
- It should be ideal for use as a side campaign that can overlay another active campaign.

---

## Example 5: A Name Worth Wearing

### Overview

- **Campaign ID:** `campaign_a_name_worth_wearing`
- **Type:** companion-linked side campaign
- **Length:** medium
- **Role:** legitimacy, identity, and public standing arc
- **Active or side campaign:** side campaign
- **Summary:** A claim, challenge, or public test forces the player to decide whether names matter because of truth or because of use.

### Entry

- Rolf is present or relevant.
- The player has entered noble-facing politics or public reputation content.
- A title, inheritance, oath, or claim is under dispute.
- There is a route to public recognition or public humiliation.

### Core choices

1. **Defend the name**
2. **Expose the lie**
3. **Rebuild the name**
4. **Use the name as a tool**

### Branches

#### Branch A — Public defense
The player publicly supports the claim.

#### Branch B — Truth over title
The player rejects false legitimacy and accepts the consequences.

#### Branch C — Reforged identity
The player turns the claim into a new form of legitimacy.

#### Branch D — Tactical use
The player uses the name as a temporary political instrument.

#### Hidden branch — Earned title
If the player behaves with enough consistency, the name becomes earned rather than inherited.

#### Failure branch — Shame spiral
If public credibility collapses, the companion or campaign may become politically brittle.

### Endings

- **Claim defended**
- **Claim exposed**
- **Claim reforged**
- **Claim exploited**
- **Earned title ending**
- **Public shame ending**

### Unlocks

- noble diplomacy content
- public ceremony scenes
- legitimacy-based campaign routes
- companion trust changes for Rolf
- broader ruler campaign access

### World effects

- Public reputation changes significantly.
- Rolf’s approval and self-image should shift based on the branch.
- Noble factions may become more or less willing to negotiate later.
- The campaign can unlock a broader legitimacy arc or close it off.

### Implementation notes

- This campaign should strongly affect Rolf and any honor-oriented companion.
- It should feed into the main political campaign if the player later chooses legitimacy.

---

## Example 6: The Honest Price

### Overview

- **Campaign ID:** `campaign_the_honest_price`
- **Type:** side campaign
- **Length:** medium
- **Role:** trade, captivity, and soft-power negotiation arc
- **Active or side campaign:** side campaign
- **Summary:** Marnid’s contacts, a trade route, or a prisoner broker create a chance to make a clean gain or a dirty one.

### Entry

- The player has a trade route, market contact, or prisoner opportunity.
- The economy or prisoner market is under pressure.
- Marnid or a similar trade-minded companion is available.
- The player can choose between profit, restraint, and reform.

### Core choices

1. **Make the deal**
2. **Break the deal**
3. **Rewrite the deal**
4. **Turn the deal against its owners**

### Branches

#### Branch A — Honest trade
The player builds a sustainable route and protects future exchange.

#### Branch B — Dirty trade
The player profits but inherits moral and political cost.

#### Branch C — Reformed trade
The player keeps the route alive but changes who benefits.

#### Branch D — Trap the brokers
The player uses the market against its own operators.

#### Hidden branch — Merchant coalition
If the player maintains enough trust and stability, a new trade coalition can emerge.

#### Failure branch — Market collapse
If the route is destroyed without a replacement, the economy or prisoner network may collapse into hostility.

### Endings

- **Clean profit**
- **Dirty profit**
- **Reformed route**
- **Broker trap**
- **Merchant coalition**
- **Market collapse**

### Unlocks

- trade access arcs
- quartermaster-related bonuses
- mercantile diplomacy
- future city and caravan content
- alternate prisoner-market follow-ups

### World effects

- Trade stability changes for the region.
- Marnid and Katrin should react strongly.
- Future market offers and caravan safety can be altered by the ending.
- The player may gain or lose underworld access depending on the branch.

### Implementation notes

- This campaign is a good medium-length economic side arc.
- It should strongly affect Marnid, Katrin, and sometimes Borcha.
- It should have a visible impact on future offers and market safety.

---

## Example 7: The Last Banner of the East

### Overview

- **Campaign ID:** `campaign_the_last_banner_of_the_east`
- **Type:** long campaign
- **Length:** long
- **Role:** endgame war campaign
- **Active or side campaign:** active or replacing crisis campaign
- **Summary:** A large eastern force or coalition crisis forces the player to choose between defense, sacrifice, and counteroffensive.

### Entry

- Midgame or late game world state.
- At least one major faction is under existential pressure.
- The player has enough army strength, political capital, or crisis relevance to matter.
- Several other campaign arcs may already have resolved.

### Core choices

1. **Hold the line**
2. **Bait the enemy**
3. **Betray a rival to survive**
4. **Build a coalition through pressure and fear**
5. **Strike first**

### Branches

#### Branch A — Defensive stand
The player attempts to preserve the line and survive the wave.

#### Branch B — Delayed strike
The player lures the enemy into overextension before counterattacking.

#### Branch C — Political sacrifice
The player gives up one power center to preserve another.

#### Branch D — Coalition pressure
The player uses diplomacy and fear to unite the surviving powers.

#### Hidden branch — Banner replacement
If the player balances legitimacy, fear, and coalition strength correctly, they can become the new dominant banner without fully collapsing the region.

#### Failure branch — Regional collapse
If key allies fall or the player waits too long, the campaign can collapse into a disaster state.

### Endings

- **Defensive victory**
- **Costly withdrawal**
- **Coalition survival**
- **Banner replacement**
- **Regional collapse**
- **Dominant power ending**
- **Sacrifice ending**

### Unlocks

- endgame campaign resolution
- postwar settlement campaigns
- late-game diplomacy
- successor campaigns for surviving factions
- empire or reconstruction arcs

### World effects

- War weariness and legitimacy should heavily influence outcomes.
- Companion morale can determine whether coalition-building succeeds.
- The branch ending should reshape the entire late-game political map.

### Implementation notes

- This campaign should be the “big war” structure.
- It should be heavily influenced by war weariness, legitimacy, and companion morale.
- It should be able to replace or override smaller side campaigns when the crisis spikes.

---

## Example write-up template

Use this when authoring a new campaign proposal.

```md
# Campaign Name

## Overview
- Campaign ID:
- Type:
- Length:
- Role:
- Active or side campaign:
- Summary:

## Entry
- Requirements:
- World state:
- Companion state:
- Faction state:

## Core choices
1. ...
2. ...
3. ...

## Branches
- Branch A:
- Branch B:
- Hidden branch:
- Failure branch:

## Endings
- Ending 1:
- Ending 2:
- Ending 3:
- Secret ending:

## Unlocks
- ...

## World effects
- ...

## Implementation notes
- Quest chain mapping:
- State flags:
- Companion reactions:
- Unlocks:
```

## Summary

These examples show the intended scale of the campaign layer:

- a campaign can be short or long
- a campaign can be moral, political, military, or companion-driven
- a campaign can unlock another campaign
- a campaign can suspend or replace the active story
- a campaign can end in several distinct ways

That is the kind of structure this repo should author now so it can be implemented later without inventing it from scratch.
