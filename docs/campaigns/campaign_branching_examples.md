# Campaign Branching Examples

> Status: **target-state** examples only.  
> This page is a design aid for campaign authors and future module-system implementation, not proof of a current campaign runtime.

## Purpose

This document shows how campaign choice structures should behave in the docs layer.

It is meant to help authors think about:

- visible player choice
- hidden branch discovery
- branch convergence
- campaign replacement
- suspended side stories
- multiple endings

It does **not** claim that a campaign engine already exists in source.

## Read this page as a pattern library

A branch example can be:

- a single choice
- a multi-stage branch
- a hidden branch
- a branch that unlocks a different campaign
- a branch that suspends or replaces the current active campaign
- a branch that collapses into failure or rupture

When you later lower campaign content into the module system, these patterns should become quest chain transitions, slot-based flags, menu conditions, and trigger-driven state changes.

---

## Pattern 1: simple binary choice

**Use when:** the campaign has one major ethical or strategic decision.

### Structure

- The player sees one clear decision.
- Each option leads to a different next chapter.
- The branches may rejoin later, but they do not have to.

### Example

**Campaign:** `campaign_mercy_under_chains`

- **Choice A:** rescue the captives
- **Choice B:** trade the captives for advantage

### Expected branch behavior

- Rescue should increase moral trust and companion approval.
- Trade should increase short-term power and moral pressure.
- The branches should both continue the campaign, but with different warning states.

### Notes

This is the cleanest branch pattern for a short side campaign.

---

## Pattern 2: binary choice with delayed consequence

**Use when:** the player’s choice should not resolve immediately.

### Structure

- The campaign presents a direct choice.
- The immediate result is small.
- The real consequence appears in the next chapter or after a delay.

### Example

**Campaign:** `campaign_chains_in_the_market`

- **Choice A:** destroy the chain
- **Choice B:** regulate the chain

### Expected branch behavior

- Immediate results are local.
- Later chapters reveal whether the market retaliates, stabilizes, or mutates underground.
- The branch should leave behind a permanent state flag.

### Notes

This pattern is good for moral or political choices that should feel “paid for” later.

---

## Pattern 3: three-way strategic branch

**Use when:** the player needs more than a simple good/bad split.

### Structure

- Path A is ideal but difficult.
- Path B is practical but compromised.
- Path C is aggressive or exploitative.

### Example

**Campaign:** `campaign_the_honest_price`

- **Choice A:** make the deal honestly
- **Choice B:** rewrite the deal
- **Choice C:** turn the deal against its owners

### Expected branch behavior

- The three branches should represent different philosophies, not just different rewards.
- Each branch should alter later campaign availability.
- At least one branch should have a hidden follow-up if the player performs well enough.

### Notes

Three-way branches are useful for trade, diplomacy, and faction management campaigns.

---

## Pattern 4: branch with a convergence point

**Use when:** the campaign should allow choice without creating infinite content split.

### Structure

- The player chooses between several paths.
- The paths diverge for a while.
- The paths rejoin at a common climax.
- The ending varies based on prior choices.

### Example

**Campaign:** `campaign_the_road_to_the_crown`

- **Legitimacy route**
- **Mercenary route**
- **Conquest route**
- **Coalition route**

All routes can converge on the same final political crisis, but the final scene should differ based on:
- legitimacy
- fear
- coalition support
- companion trust
- faction memory

### Expected branch behavior

- The campaign should not need four completely separate endgame maps.
- It should need four distinct endgame states.
- The convergence point keeps the campaign manageable while preserving reactivity.

### Notes

This is the recommended pattern for long campaigns.

---

## Pattern 5: hidden branch

**Use when:** the player should feel that strong play reveals deeper options.

### Structure

- A visible branch is presented.
- A hidden branch opens only if the player meets special conditions.
- The hidden branch should feel earned, not random.

### Example

**Campaign:** `campaign_ashes_of_the_steppe`

Hidden steppe alliance branch could open if the player:
- supports local scouts
- avoids betraying pathfinders
- keeps casualties low
- maintains enough mobile strength
- does not fully commit to exploitative behavior

### Expected branch behavior

- The hidden branch should not replace the visible choice.
- It should be an alternative route discovered through play.
- It should often represent a more nuanced or higher-skill outcome.

### Notes

Hidden branches are best used sparingly.

---

## Pattern 6: failure branch

**Use when:** the campaign should acknowledge that bad play or bad timing matters.

### Structure

- The player can ignore warnings, fail the condition, or mishandle a critical chapter.
- The campaign does not simply stop; it resolves into a failure state.

### Example

**Campaign:** `campaign_the_quiet_knife`

If the player is discovered too early or mishandles the secret:
- the campaign becomes defensive
- the leverage is lost
- rivals gain warning
- the player may be forced into a weaker ending

### Expected branch behavior

- Failure should still be a meaningful story result.
- It should never be treated as “nothing happened.”
- It may unlock a repair arc or a harder follow-up campaign.

### Notes

This is important for campaigns that involve secrecy, diplomacy, or companion trust.

---

## Pattern 7: branch that unlocks a different campaign

**Use when:** one campaign should serve as the gateway to another.

### Structure

- A branch conclusion does not just alter the same campaign.
- It opens a new campaign or campaign family.
- The unlocked campaign can be a reward, consequence, or escalation.

### Example

**Campaign:** `campaign_a_name_worth_wearing`

Possible unlocks:
- a noble legitimacy campaign
- a public claim campaign
- a broader ruler arc

### Expected branch behavior

- The choice should matter beyond the current arc.
- The unlocked campaign should inherit world state from the first one.
- The transition should feel narratively justified.

### Notes

This is one of the best ways to make campaigns feel like a connected campaign web.

---

## Pattern 8: side campaign that suspends the active campaign

**Use when:** the side story is urgent enough to interrupt the main arc.

### Structure

- The active campaign remains valid.
- A side campaign becomes the immediate focus.
- The player returns to the original campaign later, unless the side campaign changes the outcome.

### Example

**Campaign:** `campaign_mercy_under_chains`

A rescue crisis could suspend a larger war or politics campaign.

### Expected branch behavior

- The side campaign should not erase the main one unless explicitly designed to do so.
- It should alter the next step of the active campaign.
- It may create a “return with consequences” effect.

### Notes

This is the recommended pattern for companion-linked moral choices.

---

## Pattern 9: side campaign that replaces the active campaign

**Use when:** the crisis is severe enough that the player’s priorities must shift.

### Structure

- The active campaign is overtaken by a new crisis.
- The current story is effectively paused or replaced.
- The replacement campaign may later merge back or permanently terminate the old one.

### Example

**Campaign:** `campaign_the_last_banner_of_the_east`

A major invasion or coalition crisis can replace smaller arcs.

### Expected branch behavior

- The replacement should be visible and justified.
- The player should understand why the focus has changed.
- The old campaign may survive in the background, but it should not remain the active story if the crisis is truly overriding.

### Notes

This is a strong pattern for late-game world events.

---

## Pattern 10: branch with moral ambiguity

**Use when:** the campaign should avoid a simple good/evil split.

### Structure

- Every choice has cost.
- Every branch creates a different kind of damage or compromise.
- The best outcome may still be painful.

### Example

**Campaign:** `campaign_the_honest_price`

- honest trade may stabilize the route but preserve ugly systems
- dirty trade may empower the player but corrupt their allies
- reform may save lives but reduce immediate profit
- trap the brokers may create backlash

### Expected branch behavior

- No branch should feel cost-free.
- Different companions should react differently to each path.
- The campaign should use world memory to remember the compromise.

### Notes

This is ideal for trade, diplomacy, captivity, and faction management stories.

---

## Pattern 11: branch with companion conflict

**Use when:** companion approval is part of the campaign’s core tension.

### Structure

- A campaign choice favors one companion’s values and offends another’s.
- The player must choose between allies, not just options.
- Approval thresholds can influence which branch becomes available.

### Example

**Campaign:** `campaign_chains_in_the_market`

- Ymira may support rescue
- Marnid may support compromise or profit
- Firentis may accept a disciplined rescue but reject exploitation

### Expected branch behavior

- Some companions should warn before the branch breaks trust.
- Some companions should unlock or lock options based on approval state.
- The campaign should use companion reaction as a meaningful part of progression.

### Notes

This pattern should be common, not rare, because it makes the campaign layer feel personal.

---

## Pattern 12: branch with campaign switching

**Use when:** one story needs to hand off to another active story.

### Structure

- The branch conclusion changes which campaign is active.
- The current campaign may be suspended, merged, or terminated.
- The new campaign takes over the player’s narrative focus.

### Example switch types

- `suspend_and_replace`
- `overlay_and_return`
- `split_to_branch`
- `merge_back`
- `unlock_new_active`
- `terminate_old_and_start_new`

### Expected branch behavior

- Switching should be explicit in the docs.
- The player should know whether the old campaign is still alive.
- The handoff should create continuity, not confusion.

### Notes

This is a key design tool for long-running campaign arcs with interruptions.

---

## Recommended branch metadata for docs

When writing campaign examples, document branch metadata in a compact form like this:

```md
- **Branch ID:** `branch_id`
- **Trigger:** what causes the branch to appear
- **Choice:** what the player sees
- **Gate:** approval, faction memory, world state, or item/state requirement
- **Result:** immediate branch result
- **Follow-up:** next chapter or campaign unlocked
- **Risk:** what can go wrong
- **Companion impact:** who reacts strongly
```

This makes later implementation easier because the branch can be mapped to quest conditions and state checks.

## Branching checklist for authors

Before finalizing a campaign, ask:

- Does the player see enough information to choose meaningfully?
- Does each branch change later state?
- Does the branch alter companion, faction, or world memory?
- Does at least one branch unlock something new?
- Does the campaign have a failure or rupture path if appropriate?
- Do branches converge when the scope would otherwise explode?
- Is any hidden branch discoverable through play?
- Does the ending reflect the choices made earlier?

## Summary

Use branching to create campaign identity, not just content variety.

Good campaign branches should do at least one of these:

- change the active campaign
- change future unlocks
- change companion trust
- change world pressure
- change faction memory
- change the ending

If a branch does none of those, it is probably just a detour and not a real campaign choice.
