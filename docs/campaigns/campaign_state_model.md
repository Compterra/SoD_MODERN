# Campaign State Model

> Status: **target-state** design for later module-system implementation.  
> This document defines how campaign progress, branching, unlocks, and replacement should persist once the campaign layer is built.

## Purpose

Campaigns need a small, explicit state model so they can:

- remember what branch the player chose
- unlock later campaigns
- suspend or replace active campaigns
- preserve companion and faction consequences
- support multiple endings without turning every campaign into a separate subsystem

This document defines the persistence vocabulary for that layer.

## Guiding principle

Campaign state should be **compact, readable, and lowerable** into the existing Mount & Blade module system.

That means campaign state should be represented by a small number of persistent flags, slots, and tracked outcomes rather than a brand-new runtime object graph.

## Core state buckets

A campaign should be able to store state in the following buckets:

### 1. Campaign identity

What campaign is currently relevant?

- campaign ID
- active/paused/suspended/terminated status
- parent campaign ID if the campaign was unlocked by another campaign
- campaign family or campaign line ID if needed

### 2. Campaign progress

How far through the campaign is the player?

- act index
- chapter index
- current branch ID
- current beat ID
- current objective state
- current ending candidate state

### 3. Branch memory

Which important choices have already happened?

- branch flags
- branch locks
- hidden branch discovery flags
- failed branch flags
- branch rejoin flags

### 4. World impact

What did the campaign change in the world?

- faction memory flags
- diplomacy modifiers
- market or route pressure flags
- patrol or security pressure flags
- special threat pressure flags
- region or center influence flags

### 5. Companion impact

What did the campaign change in the company?

- companion approval deltas
- companion warning states
- companion trust states
- companion departure risk
- companion quest unlock flags
- companion role changes

### 6. Unlock state

What future content has this campaign enabled?

- unlocked campaign IDs
- unlocked side campaign IDs
- unlocked branch IDs
- unlocked ending IDs
- unlocked follow-up quest chains

### 7. Ending state

How did the campaign resolve?

- victory
- compromise
- rupture
- betrayal
- collapse
- exile
- domination
- secret ending
- custom ending flag

## Recommended campaign storage shape

For later implementation, each campaign should be able to persist in a compact record with fields like these:

```md
- campaign_id
- campaign_status
- campaign_family_id
- parent_campaign_id
- active_branch_id
- active_act_id
- active_chapter_id
- active_beat_id
- branch_flags
- world_flags
- companion_flags
- unlock_flags
- ending_flags
- reputation_flags
- replacement_campaign_id
- suspended_campaign_ids
```

That structure is intentionally simple enough to map to slots or a small set of quest-owned state fields.

## Recommended state types

### Active state

The campaign is currently driving the player’s story.

### Suspended state

The campaign is paused temporarily while another campaign takes the focus.

### Branch state

The campaign is still active, but the path has been redirected.

### Converged state

The campaign has rejoined its main path after a detour.

### Terminated state

The campaign has ended and will no longer advance.

## Recommended state transitions

Campaigns should transition through a small number of explicit states.

### 1. Start

Campaign becomes active after its entry conditions are met.

### 2. Branch

Player choice changes the active path.

### 3. Suspend

A side campaign temporarily pauses the current active campaign.

### 4. Replace

A new campaign takes over the active slot.

### 5. Converge

A branch or side arc returns to the main story.

### 6. Unlock

Completion or a branch opens another campaign.

### 7. End

The campaign resolves into a final state.

### 8. Archive

The result is stored for later world-state use.

## Switch vocabulary

These switch types should be documented whenever a campaign changes the active story.

- **`suspend_and_replace`**  
  Pause the current campaign and activate another one.

- **`overlay_and_return`**  
  Add a temporary side campaign that later returns control to the main story.

- **`split_to_branch`**  
  Replace the current route with a new branch line.

- **`merge_back`**  
  Rejoin the main campaign after a detour.

- **`unlock_new_active`**  
  Finish one campaign and immediately activate a new one.

- **`terminate_old_and_start_new`**  
  End one campaign and replace it with a fresh campaign line.

These are design terms for the docs. They can be lowered later into quest flags, menu conditions, and trigger logic.

## Branch flags

A campaign should not need dozens of complicated variables to remember the player’s choice.

Instead, use a small flag set such as:

- `branch_legitimacy`
- `branch_mercenary`
- `branch_conquest`
- `branch_coalition`
- `branch_rescue`
- `branch_exploit`
- `branch_hidden`
- `branch_failure`
- `branch_secret`
- `branch_reform`
- `branch_ruin`

Not every campaign uses every flag.  
The goal is to have a compact and readable vocabulary for long-form narrative state.

## Ending flags

Use ending flags to make later content react without reading the entire campaign history.

Recommended ending categories:

- `ending_victory`
- `ending_compromise`
- `ending_betrayal`
- `ending_collapse`
- `ending_exile`
- `ending_domination`
- `ending_secret`
- `ending_redemption`
- `ending_custom`

This lets later content check the result of a prior campaign without reopening all of its branches.

## Unlock rules

Campaign unlocks should follow predictable rules.

### 1. Direct unlock

Finishing campaign A unlocks campaign B.

### 2. Conditional unlock

Campaign A only unlocks campaign B if a branch or ending condition is met.

### 3. Hidden unlock

Campaign A unlocks campaign B only if the player discovers or earns a hidden outcome.

### 4. Replacement unlock

Campaign A ends and campaign B becomes the new active campaign.

### 5. Parallel unlock

Campaign A unlocks a side campaign that can run later, alongside, or during a different active arc.

## Recommended unlock metadata

When documenting unlocks, specify:

- unlock target
- unlock condition
- unlock type
- whether the unlock is permanent
- whether the unlock requires a branch outcome
- whether the unlock requires a companion state
- whether the unlock requires a faction state

Example:

```md
- **Unlock target:** `campaign_the_last_banner_of_the_east`
- **Unlock condition:** `ending_feared_ruler` or `ending_coalition_ruler`
- **Unlock type:** direct unlock
- **Permanent:** yes
- **Requires branch:** coalition or conquest
- **Requires companion state:** at least two steady companions
- **Requires faction state:** one major faction hostile or fractured
```

## Companion state model

Companion-related campaign state should remain distinct from the campaign branch itself.

Recommended companion state values:

- **steady** — the companion supports the campaign path
- **wary** — the companion accepts the campaign but is uneasy
- **troubled** — the companion may warn or challenge the player
- **near breaking** — the companion may refuse to continue
- **broken** — the companion has rejected the player’s path
- **redeemed** — the companion recovered trust after a difficult choice

Campaigns should use these states to gate campfire lines, warnings, and companion-linked branches.

## Faction state model

Campaigns should also store simplified faction reaction states.

Recommended faction values:

- **friendly**
- **neutral**
- **suspicious**
- **hostile**
- **afraid**
- **respectful**
- **exhausted**
- **fractured**
- **retaliating**

These are not meant to replace diplomacy.  
They are meant to give campaigns a quick way to remember how the world reacted.

## Example state flow

Here is an example of how a campaign might move through states.

### Example: a loyalty-heavy campaign

1. Campaign starts active.
2. Player chooses a mercy branch.
3. One companion becomes steady, another becomes troubled.
4. A side campaign suspends the main arc.
5. The side campaign ends with a compromise.
6. The main campaign returns with altered faction memory.
7. The ending becomes a compromise ending rather than a victory ending.
8. The campaign unlocks a redemption follow-up.

This is the kind of story persistence the campaign layer should support.

## Storage guidance for later implementation

When this is lowered later, prefer:

- a small number of global or quest-owned campaign slots
- compact bit flags for branch memory
- separate state records for companion and faction impacts
- explicit unlock flags rather than inferred unlock logic
- readable campaign IDs and branch IDs

Avoid:

- giant freeform campaign blobs
- ambiguous state that cannot be queried cheaply
- hidden logic that only lives in one trigger
- state transitions that are not documented in the campaign record

## Recommended authoring checklist

Before a campaign is considered documented, confirm:

- the active campaign can be identified
- the branch choices are named
- the state transition type is documented
- the ending states are named
- the unlock targets are listed
- the companion and faction effects are stated
- the replacement or suspension behavior is clear

## Summary

The campaign state model should make the macro layer feel persistent without making it unmanageable.

The key idea is simple:

- **campaigns change state**
- **state changes branches**
- **branches change endings**
- **endings unlock or alter later campaigns**

That gives the game a campaign structure even though the base module system does not provide one natively.
