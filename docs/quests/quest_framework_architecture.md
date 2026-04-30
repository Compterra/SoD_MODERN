# Quest Framework Architecture

> Status: **current implementation** for the hybrid quest model documented here; **target-state** language is used only where the audited source does not yet prove a broader ontology.

This page explains the documented architecture of the quest framework as it exists in the source-backed model and the build pipeline. It is intentionally narrower than a full game-wide quest ontology.

## Scope note

- **current implementation**: the hybrid quest model already present in the repository, including schema-backed helpers, legacy tuple fragments, and build-time lowering.
- **target-state**: broader ontology language, richer branching semantics, or any generalized actor/NPC subsystem that is not explicitly proven by the audited source.
- **build-time verification**: checks performed by the quest build pipeline, not a runtime diagnostics system.

Primary source anchors for this page:

- [`src/quests/quest_schema.py`](../../src/quests/quest_schema.py)
- [`src/quests/quest_runtime.py`](../../src/quests/quest_runtime.py)
- [`build/build_quests.py`](../../build/build_quests.py)
- [`docs/quests/runtime_event_audit.md`](./runtime_event_audit.md)

## Architecture at a glance

The quest framework is documented as a layered system:

1. **Authoring layer**  
   Schema-backed helpers and legacy tuple fragments describe quest content.
2. **Build layer**  
   `build/build_quests.py` lowers schema-backed fragments into the legacy compiler output shape.
3. **Runtime layer**  
   `src/quests/quest_runtime.py` exposes lifecycle terms and audited hook handling.
4. **Integration seams**  
   Event seams, storage categories, and build-time verification connect the quest content to the rest of the module.

That layered model is evidence-backed. A broader formal ontology is not claimed here unless a source file explicitly proves it.

## Domain-model mapping

The table below maps the canonical nouns used in these docs to the audited symbols and categories that are actually visible in source or build output.

| Canonical noun used in docs | Audited symbol / category | Current implementation meaning | Notes |
| --- | --- | --- | --- |
| Quest chain | `quest_chain(...).as_legacy_tuples()` export path | The compatibility export shape produced by the authoring layer | This is the documented bridge from helpers to legacy tuples. |
| Schema-backed fragment | Schema-backed quest fragment helper | Authoring-time structure that is lowered during the build | Use this term only for source-backed helper output. |
| Legacy tuple fragment | Legacy quest tuple fragment | Direct tuple-shaped content already accepted by the legacy pipeline | This is part of the current implementation. |
| Quest-owned state | Quest-owned storage category | State that belongs to an individual quest record | Keep this distinct from mirror and temporary state. |
| Mirror state | World/party-visible mirror storage category | State duplicated into a visible or mirrored game-space record | This is a storage category, not a full actor model. |
| Quest-giver memory | Quest-giver-associated storage category | Memory or bookkeeping associated with a quest giver | This is narrower than a broad NPC subsystem. |
| Temporary state | Temporary or ephemeral storage category | Short-lived data used during quest evaluation or build lowering | Do not describe this as durable quest state. |
| Runtime hook | Audited seam / lifecycle hook | A documented runtime entry point used by the quest runtime | The audit covers seams, not a unified dispatcher claim. |
| Lifecycle term | `handle_hook`, `advance_stage`, `complete`, `fail`, `abort` | The documented runtime vocabulary for quest progression and outcomes | Do not infer extra public APIs from these terms. |
| Broader quest ontology | Target-state model | A more formalized model of actors, branches, and progression relationships | Treat as target-state unless a source file explicitly proves it. |

## Current implementation

The audited source supports a hybrid model:

- Legacy tuple fragments still exist and remain part of the compatibility path.
- Schema-backed fragments are lowered into the legacy compiler output during build.
- The quest runtime uses a small lifecycle vocabulary rather than a full state-machine API.
- Storage is described in categories, not as a general-purpose NPC subsystem.

This is the current implementation surface that the rest of the documentation should treat as authoritative.

## Storage taxonomy

The storage taxonomy is intentionally narrow and should be read as a quest-state discipline, not as a universal AI or NPC framework.

### 1. Quest-owned state

Quest-owned state is the primary authoritative record for the quest itself. It belongs to the quest instance and should be treated as the source of truth for quest progression.

### 2. Mirror state

Mirror state is a replicated or visible representation used by the broader game world, party, or scene logic. It is useful for presentation or compatibility, but it is not the source of truth when the quest-owned record exists.

### 3. Quest-giver memory

Quest-giver memory is the storage associated with the giver of the quest. In this documentation set, that means quest-giver bookkeeping and remembered quest-related facts, not a broad NPC behavior system.

### 4. Temporary state

Temporary state is short-lived and local to a runtime decision, build step, or transition. It should be cleaned up or discarded when the current operation completes.

## Integration seams

The architecture is built around a few documented seams:

- **Authoring seam**: schema-backed helpers and legacy tuples can coexist in the same source package.
- **Build seam**: `build/build_quests.py` lowers the mixed representation into the legacy export shape.
- **Runtime seam**: `src/quests/quest_runtime.py` provides the lifecycle vocabulary and hook handling.
- **Event seam**: audited battle, mission, dialogue, hourly, daily, and frame hooks are documented in [`runtime_event_audit.md`](./runtime_event_audit.md).
- **Storage seam**: quest-owned, mirror, giver-memory, and temporary categories keep state responsibilities separate.

These seams are part of the current implementation. A broader ontology that merges them into a single generalized model is target-state language only.

## Target-state boundaries

The following ideas are intentionally left in target-state language unless another source file explicitly proves them:

- a fully formalized quest state machine
- a generalized NPC subsystem
- a universal branch graph API
- a single dispatcher that is claimed to wire every audited seam together

Use the current audited categories and lifecycle terms when describing the implementation that exists today.

## Reader guidance

If you are moving between the phase-18 documentation pages, use this page as the architecture summary, then follow the links below:

- [`Quest Runtime API`](./quest_runtime_api.md)
- [`Runtime Event Audit`](./runtime_event_audit.md)
- [`Quest Branching Examples`](./quest_branching_examples.md)

For roadmap context, see:

- [`Quest Framework Overview`](./quest_framework_overview.md)
- [`Quest Framework Master Plan`](./quest_framework_master_plan.md)