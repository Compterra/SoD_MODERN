# Quest State Storage Audit

> **Status:** current implementation audit. This document describes the storage categories that are visible in the audited quest runtime and lowering path. It does **not** claim a general NPC subsystem.

This audit narrows the storage discussion to the categories that are already relevant to the quest framework:

- quest-owned authoritative state
- quest-giver memory and other mirror state
- world / party mirrors
- temporary / global state used during quest execution
- cleanup boundaries at completion, failure, abort, and stage transitions

The aim is to keep the storage taxonomy precise so phase 5 reads as **storage discipline** rather than a broader NPC or world-state architecture.

## Current implementation vs target-state

| Label | Meaning in this document |
| --- | --- |
| current implementation | Behavior that is already visible in the audited quest runtime or in build-time lowering. |
| target-state | A roadmap expectation, pattern, or cleanup rule that is useful for authors but is not proven as a unified runtime API. |
| not yet implemented | A future behavior that should not be read back into the current source. |

## What this audit covers

This audit covers the storage categories that quest content can rely on today:

1. **Quest-owned state** — the authoritative record for a quest.
2. **Mirror state** — data mirrored onto a giver, party, world object, or other visible container so the quest can be observed from more than one place.
3. **Quest-giver memory** — giver-specific bookkeeping that records interaction or availability, without implying a general NPC subsystem.
4. **Temporary state** — short-lived values used during handling, transition, or cleanup.
5. **Global or world-scoped state** — shared values that are visible outside one quest, when the quest design needs them.

The audit is intentionally conservative: if a state category is only useful as a design target, it is labeled as **target-state** below.

## Storage taxonomy

| Category | current implementation | Visibility / purpose | Cleanup expectation |
| --- | --- | --- | --- |
| Quest-owned authoritative state | The primary quest record and the values lowered into the legacy quest output. | Holds the actual quest progress, branch decisions, counters, and flags that define the quest. | Cleared or finalized when the quest is completed, failed, or aborted. |
| Quest-giver memory | Giver-specific memory used to remember that the player interacted, accepted, declined, or exhausted a line of availability. | Keeps giver-facing quest facts visible without turning the giver into a general NPC state machine. | Should be reset or refreshed when the quest is removed or the giver is no longer relevant. |
| World / party mirrors | Mirror values attached to the world, a party, or similar visible container. | Exposes quest state to the places that need to react to it. These mirrors are not authoritative. | Should be synchronized from authoritative state and removed when the quest no longer needs public visibility. |
| Temporary state | Short-lived flags, counters, or working values used while handling a hook or moving between stages. | Helps the runtime evaluate a transition without permanently changing the quest record. | Should not survive past the handling window unless deliberately copied into authoritative state. |
| Global / shared state | Shared quest-related values that are intentionally broader than one quest. | Useful for campaign-level gating, shared visibility, or compatibility with legacy lowering. | Must be treated carefully so it does not replace quest-owned state by accident. |

## Authoritative quest state

The authoritative quest state is the center of the storage model.

It should answer questions such as:

- What stage is the quest on?
- Has the quest been completed, failed, or aborted?
- Which branch or temporary decision has already been committed?
- Which quest-owned values must survive across events?

If a value is needed to define the quest outcome, it belongs here first. Mirror state may exist for visibility, but it should always be derived from or synchronized with this authoritative record.

## Mirror state

Mirror state exists so the quest can be observed outside the quest record itself.

Typical mirror locations include:

- quest givers
- parties
- world-scoped containers
- other visible state holders used by the quest framework

This is where the documentation should stay careful:

- mirror state is **not** the same thing as the quest record
- mirror state is **not** a claim that the source has a general NPC subsystem
- mirror state is **not** the place to store logic that should remain quest-owned

Mirror state is useful when the quest must remain visible to a giver or to the world while the authoritative record stays elsewhere.

## Quest-giver memory

The older audit language sometimes made giver storage sound like a broad NPC model. That is too strong for the current source.

The safer reading is:

- the framework can retain **quest-giver memory**
- that memory is about quest interaction and availability
- it does not imply a full personality, schedule, or behavior system

Use this category when the quest must remember that a giver has already spoken, offered, declined, or otherwise responded to quest progress. Keep the scope narrow and tied to quest visibility only.

## Temporary and cleanup state

Temporary state is the place for values that exist only while the runtime is handling a specific hook or transition.

Examples of the intended discipline:

- use temporary state for intermediate calculations
- copy only the needed result into authoritative state
- clear transient values when the quest advances, completes, fails, or aborts

This keeps the runtime from accumulating accidental state that looks permanent but is only a byproduct of event handling.

## Cleanup boundaries

The audited runtime vocabulary that matters for cleanup is narrow:

- `handle_hook`
- `advance_stage`
- `complete`
- `fail`
- `abort`

These are the lifecycle terms that the documentation should use. The audit does **not** claim a formal state-machine API beyond that vocabulary.

Cleanup should be reasoned about in terms of those lifecycle outcomes:

- **advance_stage**: transient handling data should not leak into the next stage unless it is intentionally promoted
- **complete / fail / abort**: quest-owned and mirror state should be finalized or removed according to the quest’s storage category
- **handle_hook**: temporary state should stay temporary unless the handler explicitly commits it

## What this is not

This audit is **not**:

- a general NPC subsystem design
- a promise that every mirror is already implemented by one shared dispatcher
- a claim that all storage categories have the same lifecycle
- a new API proposal

It is a storage taxonomy for the **current implementation** plus clear boundaries for the **target-state** cleanup discipline.

## Practical reading guide

When reviewing quest content or runtime behavior, use this ordering:

1. identify the **authoritative quest state**
2. identify any **mirror state** that exists for visibility
3. separate **quest-giver memory** from broader NPC behavior
4. classify short-lived values as **temporary state**
5. treat any broader design wish-list as **target-state** until the source proves it

That keeps phase 5 grounded in storage discipline and prevents the audit from being read as a full NPC architecture.