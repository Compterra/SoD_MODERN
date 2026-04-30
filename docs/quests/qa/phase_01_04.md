# QA Report: Quest Framework Phases 1-4

## Scope

Reviewed against:

- `docs/quests/quest_framework_master_plan.md`
- `docs/quests/quest_framework_overview.md`
- `docs/quests/quest_architecture_audit.md`
- `docs/quests/runtime_event_audit.md`
- `docs/quests/quest_state_storage_audit.md`
- `docs/quests/quest_framework_architecture.md`
- `docs/quests/quest_runtime_api.md`
- `src/quests/quest_schema.py`
- `src/quests/quest_runtime.py`

This report stays diagnostic only. It distinguishes current behavior from target-state language and flags any wording that appears to outrun the audited source vocabulary.

## Verdict Summary

| Phase | Verdict | Summary |
| --- | --- | --- |
| Phase 1 architecture audit | pass | The architecture baseline is documented directly and consistently across the audit and consolidated architecture docs. |
| Phase 2 domain model | partial | The schema vocabulary is present, but the docs still mix current symbols with broader domain language that is not yet normalized into a single canonical model. |
| Phase 3 state machine | partial | Runtime lifecycle terminology exists, but the docs do not yet justify a fully formalized quest state-machine model. |
| Phase 4 event-driven progression | partial | Event seams are documented, but some wording can still read as if end-to-end progression wiring is already complete. |

## Phase 1 — architecture audit

**Verdict: pass**

### Current behavior
- `docs/quests/quest_architecture_audit.md` already documents the current architecture baseline in audit style.
- `docs/quests/quest_framework_architecture.md` restates the layered architecture in consolidated form without changing the underlying vocabulary.
- `docs/quests/quest_framework_overview.md` gives readers a navigation path into the architecture material.

### Target behavior
- The phase 1 roadmap item is satisfied when the documentation explains the current architectural seams clearly enough for later phases to build on them.
- That is already the case: the docs describe the quest framework as a layered system with explicit authoring/runtime/build boundaries.

### Unsupported or overextended claims
- The only risk here is wording drift: phase 1 should stay framed as an **audit/baseline**, not as a claim that the architecture is finalized or immutable.
- If any paragraph in the consolidated architecture doc sounds like a completed design spec rather than an audit of current structure, it should be softened.

### Smallest doc fix
- Add or preserve a short sentence in the overview or architecture doc that says phase 1 is a **current-state audit**, not a final architecture freeze.

## Phase 2 — domain model

**Verdict: partial**

### Current behavior
- `src/quests/quest_schema.py` is the source anchor for schema-backed quest vocabulary.
- The phase-18 architecture doc and the authoring/runtime docs reference schema-backed fragments, legacy fragment lowering, and runtime-facing terminology.
- The storage audit also contributes to the model by separating quest state categories from authoring structure.

### Target behavior
- Phase 2 wants a stable domain model vocabulary that readers can treat as canonical across authoring, runtime, and storage discussions.
- The current docs partially provide that, but the model is still distributed across several documents rather than centralized in one authoritative glossary or symbol map.

### Unsupported or overextended claims
- Any text that implies the project already has a fully normalized quest ontology is stronger than the current source vocabulary supports.
- The docs still rely on mixed terms such as schema-backed fragments, legacy fragments, runtime lifecycle terms, and storage categories. That is workable, but it is not yet a single clean domain model.
- If a reader can interpret a term as a public, stable domain entity while the source only exposes a fragment or helper-level symbol, that wording is too strong.

### Smallest doc fix
- Add a compact domain-model mapping table that ties the canonical nouns used in the docs to the actual symbols or categories in `src/quests/quest_schema.py`.
- Mark any broader nouns that are still target-state as such, instead of presenting them as fully normalized current terms.

## Phase 3 — state machine

**Verdict: partial**

### Current behavior
- `src/quests/quest_runtime.py` and `docs/quests/quest_runtime_api.md` describe runtime lifecycle behavior.
- The storage audit gives the supporting state categories and cleanup expectations.
- The docs are enough to explain that quests move through runtime phases, but not enough to prove a formal state-machine implementation with a closed transition graph.

### Target behavior
- Phase 3 implies a deterministic state machine: identifiable states, defined transitions, and clear ownership of each transition.
- The current documentation set gestures at that idea, but it does not yet present it as a fully audited machine with an explicit transition matrix.

### Unsupported or overextended claims
- Any wording that reads as though there is already a first-class quest state-machine API should be treated cautiously.
- The runtime material is lifecycle-oriented; it does not, by itself, prove a formal state machine in the stricter sense.
- Docs should not imply that all state transitions are automated or centrally enforced unless the source explicitly shows that behavior.

### Smallest doc fix
- Add a concise transition table or a short “current lifecycle only” note in `docs/quests/quest_runtime_api.md`.
- If the docs want to keep state-machine language, explicitly tag it as **target-state** unless the transition is visible in `src/quests/quest_runtime.py`.

## Phase 4 — event-driven progression

**Verdict: partial**

### Current behavior
- `docs/quests/runtime_event_audit.md` is the strongest evidence for this phase: it maps gameplay seams to runtime event categories.
- The architecture and runtime docs reinforce that quest progression is driven through event-triggered seams rather than through a monolithic polling loop.
- This is enough to document the trigger surface, but not enough to claim the whole progression pipeline is fully unified.

### Target behavior
- Phase 4 wants event-driven progression to be understood as a coherent system.
- The current docs support the idea of event-driven progression, but they still read more like an audit of hooks and seams than a complete progression specification.

### Unsupported or overextended claims
- Any sentence that implies all event sources already feed a single, complete quest progression system is too strong.
- The current docs support “audited seams” and “runtime trigger categories”; they do not fully prove that every listed event source is wired to the same progression logic today.
- If the docs name battle, mission, dialogue, or periodic triggers as if they are all equally mature current APIs, that should be narrowed to the documented surface only.

### Smallest doc fix
- Add a support matrix in `docs/quests/runtime_event_audit.md` that separates:
  - current audited hooks,
  - documented runtime seams,
  - and target-state event hooks.
- Use the same labels in `docs/quests/quest_runtime_api.md` so readers do not mistake a seam list for a complete implementation guarantee.

## Cross-phase findings

### Terminology drift to watch
- **Audit vs spec**: phase 1 material is strongest when it stays audit-driven.
- **Domain model vs fragment vocabulary**: phase 2 still needs a tighter mapping from abstract nouns to actual schema symbols.
- **State machine vs lifecycle**: phase 3 should avoid implying a stricter machine than the runtime source demonstrates.
- **Event-driven progression vs trigger list**: phase 4 should clearly separate hook inventory from end-to-end behavior.

### Most useful documentation fix overall
Add a shared “current / target / not yet implemented” label convention across the phase-18 docs and the earlier audit docs. That would let the docs keep their roadmap language without overclaiming implementation completeness.

## Final assessment

- **Phase 1** is documented well enough to count as a pass.
- **Phases 2-4** are documented, but each still mixes current source vocabulary with broader roadmap language.
- The main risk is not missing content; it is terminology that can be read as more formalized, more complete, or more API-like than the audited source currently proves.