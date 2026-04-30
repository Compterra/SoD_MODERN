# Quest Framework QA Report: Phases 5-8

## Scope

This report reviews the current quest documentation and source vocabulary against the roadmap phases listed in `docs/quests/quest_framework_master_plan.md`:

- Phase 5 — NPC state system
- Phase 6 — Dynamic quest generation
- Phase 7 — Authoring DSL/helpers
- Phase 8 — Validation/diagnostics

## Evidence reviewed

- `docs/quests/quest_framework_master_plan.md`
- `docs/quests/quest_authoring_audit.md`
- `docs/quests/quest_state_storage_audit.md`
- `docs/quests/quest_dynamic_generation_rules.md`
- `docs/quests/quest_authoring_guide.md`
- `docs/quests/quest_content_examples.md`
- `docs/quests/quest_migration_checklist.md`
- `build/build_quests.py`
- `src/quests/quest_schema.py`

## Verdict key

- **pass** — the phase is documented in a way that matches the current source vocabulary and does not overstate implementation
- **partial** — the phase is covered, but the docs mix current behavior with target-state language or use terminology that is broader than the source actually supports
- **gap** — the docs mainly describe intended behavior, but the current source vocabulary does not yet support the phase as written

## Summary verdicts

| Phase | Verdict | Short reason |
| --- | --- | --- |
| Phase 5 — NPC state system | **partial** | State storage is documented, but the docs still read like a broader NPC-state system than the audited source vocabulary clearly exposes. |
| Phase 6 — Dynamic quest generation | **gap** | The rules are documented as a target model, but the current source/build vocabulary does not present a first-class generation API. |
| Phase 7 — Authoring DSL/helpers | **partial** | Helper-style authoring is documented, but several passages imply a user-facing DSL or callable surface that is not clearly present in source. |
| Phase 8 — Validation/diagnostics | **partial** | Build-time validation is documented, but “diagnostics” overstates the current pipeline unless it is explicitly labeled as compile-time only. |

## Phase 5 — NPC state system

### Assessment

**Verdict: partial**

`docs/quests/quest_state_storage_audit.md` gives useful coverage of quest-adjacent state buckets and cleanup expectations, and that is the strongest current evidence for phase 5. However, the wording still needs to stay aligned with the audited source vocabulary in `src/quests/quest_schema.py` and `src/quests/quest_runtime.py`. The current docs are strongest when they describe **state storage taxonomy** and weaker when they imply a complete, first-class **NPC state system**.

### What is covered

- The docs clearly discuss state categories and persistence boundaries.
- Cleanup expectations and mirror rules are already documented.
- The audit-style framing is concrete and fits the current implementation vocabulary.

### Mismatches / drift

- “NPC state system” reads broader than the current source surface unless the docs explicitly narrow it to storage categories and quest-visible state mirrors.
- Any phrasing that suggests autonomous NPC lifecycle management, per-NPC state machines, or generalized NPC persistence goes beyond the audited vocabulary.
- If the docs describe this as a game-wide system rather than a quest storage concern, that is an overclaim.

### Smallest doc fixes

- Add an explicit status label such as **current storage model** vs **future NPC-state expansion**.
- When discussing NPC state, anchor the language to `docs/quests/quest_state_storage_audit.md` instead of implying a broader runtime feature.
- Avoid using “system” unless the text also says this is a storage taxonomy, not a new runtime API.

## Phase 6 — Dynamic quest generation

### Assessment

**Verdict: gap**

`docs/quests/quest_dynamic_generation_rules.md` is valuable, but it reads primarily as a **target rules document**. Based on the current build/source vocabulary available in `build/build_quests.py` and `src/quests/quest_schema.py`, the documentation should not be read as evidence of a first-class runtime quest-generation API.

### What is covered

- The document lays out generation inputs and cooldown expectations.
- It provides a clear target model for when quests may be generated and what constraints should apply.
- The rules are useful as design guidance for later implementation or lowering.

### Mismatches / drift

- The current wording can be read as if dynamic generation is already a callable system, but the source vocabulary does not clearly support that interpretation.
- If the docs imply that generation happens through a dedicated quest-generation function, that is unsupported by the audited source surface.
- If the build pipeline is described as “generating quests” rather than lowering or validating quest fragments, the terminology is too strong.

### Smallest doc fixes

- Mark the document explicitly as **target-state generation rules**.
- Replace any “the system generates” phrasing with “the roadmap expects” or “the target design uses.”
- If build-time lowering is the only current mechanism, say that directly and link it to `build/build_quests.py`.

## Phase 7 — Authoring DSL/helpers

### Assessment

**Verdict: partial**

`docs/quests/quest_authoring_guide.md`, `docs/quests/quest_content_examples.md`, and `docs/quests/quest_authoring_audit.md` together provide a credible authoring story. The main issue is terminology drift: the docs sometimes read as though there is a stable, user-facing **DSL** when the current source vocabulary in `src/quests/quest_schema.py` is better described as **schema-backed fragments/helpers**.

### What is covered

- The guide and examples give authors concrete structure to follow.
- The docs are consistent with a helper-based authoring model.
- The audit framing supports schema-backed content rather than ad hoc string assembly.

### Mismatches / drift

- “DSL” is potentially too strong unless the source actually exposes a parser or dedicated language layer.
- Any wording that implies freely callable authoring APIs should be checked against `src/quests/quest_schema.py`.
- The examples should be read as authoring patterns, not proof of a broad runtime API surface.

### Smallest doc fixes

- Prefer **authoring helpers** or **schema-backed fragment helpers** over “DSL” unless the text is explicitly about a future language layer.
- Add a short note that examples show supported authoring shapes, not a separate runtime API.
- Cross-link the guide to the schema source so readers can distinguish current helper names from future convenience layers.

## Phase 8 — Validation/diagnostics

### Assessment

**Verdict: partial**

`build/build_quests.py` appears to support build-time validation language, and `docs/quests/quest_migration_checklist.md` helps frame compatibility and verification steps. The gap is that “validation/diagnostics” can imply richer runtime diagnostics than the current pipeline vocabulary likely supports.

### What is covered

- Validation is clearly part of the build workflow.
- The migration checklist gives authors a concrete place to verify compatibility.
- The docs already point readers toward the build path rather than leaving validation undefined.

### Mismatches / drift

- If the docs use “diagnostics” without saying “build-time” or “compile-time,” they overpromise.
- A diagnostics label can imply interactive error reporting, runtime inspection, or richer tooling than the current pipeline exposes.
- The docs should avoid implying that validation is a separate runtime subsystem if the current implementation is only a build step.

### Smallest doc fixes

- Rename the phase description to **validation and build-time verification** wherever possible.
- Tie all validation claims to `build/build_quests.py`.
- Keep `docs/quests/quest_migration_checklist.md` focused on author-facing checks, not on a broader diagnostic framework.

## Cross-cutting terminology issues

### Terms that should be used carefully

- **NPC state system** — use only if the text is clearly about state storage taxonomy and not a new runtime subsystem.
- **Dynamic generation** — label as target-state unless the source actually exposes a generation API.
- **DSL** — use only if the docs truly describe a language layer; otherwise say helpers or fragments.
- **Diagnostics** — qualify as build-time or compile-time unless runtime tooling exists in source.

### Suggested global doc language

The smallest safe wording pattern for these phases is:

- **current implementation** for what the source actually does today
- **target-state** for roadmap behavior
- **build-time validation** for anything tied to `build/build_quests.py`
- **schema-backed helpers/fragments** for authoring surfaces in `src/quests/quest_schema.py`

## Final recommendation

For phases 5-8, the documentation set is strongest when it stays audit-driven and explicitly separates current source vocabulary from roadmap intent. The main cleanup needed is not new content, but **status labels and terminology tightening** so the docs stop implying that target behaviors are already callable APIs.