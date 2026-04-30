# Quest Dynamic Generation Rules

> **Status:** **target-state** generation rules. This document describes the roadmap expectations for quest generation and refresh behavior. It does **not** describe current runtime behavior except where it refers to build-time lowering or the existing threat-board vocabulary.

Use this document as a design reference, not as proof that a runtime generator already exists.

## Current implementation anchors

Only two ideas in this area should be read as current-behavior anchors:

1. **Build-time lowering** — authored quest fragments are lowered into legacy quest output by the build pipeline.
2. **Threat-board vocabulary** — the roadmap uses threat-board language to describe how a future generator should prioritize or select content.

Everything else in this document is **target-state** unless the source explicitly proves otherwise.

## Current implementation vs target-state

| Label | Meaning in this document |
| --- | --- |
| current implementation | Build-time lowering and the audited quest vocabulary that already exists in source. |
| target-state | A future generation rule, selection policy, or refresh behavior described by the roadmap. |
| not yet implemented | A generator, dispatcher, or runtime refresh path that is not present in current source. |

## Scope note

This document does not introduce a new generation API and does not imply a separate NPC subsystem.

The roadmap expects future generation behavior to remain compatible with the quest storage taxonomy documented in [docs/quests/quest_state_storage_audit.md](docs/quests/quest_state_storage_audit.md):

- quest-owned authoritative state stays authoritative
- mirror state exists for visibility only
- quest-giver memory stays narrow
- temporary state does not become permanent by accident

## Target-state generation model

The roadmap expects future quest generation to behave as a layered rule system:

1. evaluate quest availability and storage prerequisites
2. inspect world, party, and giver-facing mirrors
3. compare the current situation against threat-board priorities
4. select or refresh quest content according to authored rules
5. lower the selected content into the compatibility shape used by the build pipeline

That sequence is a **target-state** model. The current source only proves the lowering step.

## Rule categories

### 1. Availability rules

A future generator should only consider quests that satisfy their availability conditions.

These rules may include:

- progress gating
- giver availability
- world or party conditions
- compatibility checks against existing quest-owned state

**Current implementation anchor:** build-time lowering can already preserve authored condition shapes in the exported quest fragments.

### 2. Priority rules

The roadmap expects future generation to choose among candidates using priority or threat-board weighting.

Threat-board language should be treated as a selection vocabulary, not as proof of a runtime scoring engine.

Possible target-state uses include:

- selecting the next quest to offer
- deciding whether a quest should refresh
- comparing multiple candidate quests against one another

### 3. Visibility rules

A future generator should respect which storage category is visible to which part of the game state.

Examples of target-state visibility discipline:

- quest-owned state remains the source of truth
- giver mirrors may expose whether a quest is available
- world or party mirrors may expose campaign-level consequences
- temporary state should not be visible beyond the handling window

### 4. Refresh rules

The roadmap expects generated quests to be able to refresh or re-evaluate when the game state changes.

This is still **target-state**. The current source does not prove a unified runtime refresh loop.

If a design note says the system “refreshes,” read that as:

- a future generator should re-evaluate state
- the current build only lowers authored content
- any runtime refresh behavior is **not yet implemented** unless source-backed

## Threat-board concepts

The threat-board is the main target-state vocabulary for future generation priority.

Use it to describe:

- what a future generator should pay attention to
- how candidate quests could be ranked
- what kind of campaign pressure should trigger new content

Do **not** use threat-board language to imply that the current runtime has a fully wired dispatch or selection system. It is an **audited seam** in the design vocabulary, not a claim that one unified generator already exists.

## Build-time lowering and compatibility

Build-time lowering is the only currently verified path in this area.

That means:

- authored quest fragments are prepared for legacy output
- the build pipeline preserves compatibility shapes
- documentation can describe future generation rules without claiming runtime execution

When this document says “the roadmap expects,” it means the behavior belongs to the target-state design and should not be read as a current runtime guarantee.

## Not yet implemented behaviors

The following are intentionally described as **not yet implemented** unless the source proves them elsewhere:

- a unified quest generator
- a runtime threat-board dispatcher
- automatic NPC-level quest synthesis
- a live refresh loop for all quest categories
- a broader diagnostics or editor subsystem for generation

## Reading guidance

Use the following interpretation rules when reading this document:

- if a sentence says **the roadmap expects**, it is target-state
- if a sentence says **a future generator should**, it is target-state
- if a sentence refers to build-time lowering, it is current implementation
- if a sentence refers to threat-board concepts, it is design vocabulary unless source-backed runtime behavior is present
- if a sentence claims a runtime generator, treat it as **not yet implemented** unless the source proves it

## Summary

Phase 6 should be read as a **target-state generation rule set** with one current implementation anchor: build-time lowering.

That keeps the document useful for planning while preventing readers from mistaking the roadmap for an already-deployed runtime system.