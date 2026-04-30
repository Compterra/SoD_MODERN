# QA Report: Quest Framework Roadmap Phases 9-12

## Scope

Reviewed against the current quest documentation and source vocabulary:

- `docs/quests/quest_framework_master_plan.md`
- `docs/quests/quest_framework_architecture.md`
- `docs/quests/quest_runtime_api.md`
- `docs/quests/runtime_event_audit.md`
- `docs/quests/quest_branching_examples.md`
- `docs/quests/quest_build_pipeline.md`
- `docs/quests/quest_framework_overview.md`
- `src/quests/quest_runtime.py`
- `build/build_quests.py`
- `src/mission_templates/0042_jotnar_clan_arena/jotnar_clan_arena.py`

This report is diagnostic only. It does not propose implementation changes.

## Verdict summary

| Phase | Phase name | Verdict | Current vs. target | Main QA note |
| --- | --- | --- | --- | --- |
| 9 | script/compiler integration | pass | current implementation | The build docs and build source support a real build-time lowering path; wording should stay grounded in that pipeline. |
| 10 | battle-integrated quest actions | partial | mixed | The docs show battle/mission seams and a concrete mission template, but not a dedicated battle action API surface. |
| 11 | quest journal and concurrency | partial | mixed | Journal behavior is documented; concurrency is not clearly supported by the current source vocabulary. |
| 12 | branching quest chains | partial | target-heavy | Branching is documented as an example pattern, not as a stable current API. |

## Phase-by-phase findings

### Phase 9: script/compiler integration

**Verdict: pass**

**Evidence supporting current coverage**
- `docs/quests/quest_build_pipeline.md` describes the quest build path as a build-time pipeline.
- `build/build_quests.py` exists as the implementation anchor for that pipeline.
- The broader architecture docs frame quest content as schema-backed fragments that are lowered into legacy compiler output rather than introducing a brand-new runtime compiler surface.

**QA assessment**
- The current documentation set is sufficient to justify the roadmap language for script/compiler integration **if** that language is read as build-time integration.
- I did not find evidence in the reviewed source vocabulary that would support a separate runtime compiler API, and the docs should avoid implying one.

**Small terminology caution**
- Prefer wording like “build-time lowering,” “quest build pipeline,” or “legacy compiler output.”
- Avoid wording that sounds like a new callable compiler subsystem.

---

### Phase 10: battle-integrated quest actions

**Verdict: partial**

**Evidence supporting current coverage**
- `docs/quests/runtime_event_audit.md` maps gameplay events to quest/runtime seams, including battle- and mission-adjacent triggers.
- `src/mission_templates/0042_jotnar_clan_arena/jotnar_clan_arena.py` is a concrete example of mission-side integration already named by the audits.
- `docs/quests/quest_framework_architecture.md` and `docs/quests/quest_runtime_api.md` keep the runtime discussion grounded in event flow rather than standalone quest actions.

**Mismatch / overclaim risk**
- The current docs support **integration through mission/event hooks**, not a generalized “battle quest actions” API.
- If any roadmap language reads as though battle quest actions are callable anywhere in the runtime, that is too strong for the reviewed source vocabulary.

**Current vs. target**
- Current: event/mission seam integration.
- Target: a richer battle-action layer, if that is what the roadmap intends.

---

### Phase 11: quest journal and concurrency

**Verdict: partial**

**Evidence supporting current coverage**
- `src/quests/quest_runtime.py` and `docs/quests/quest_runtime_api.md` cover runtime lifecycle and journal-related behavior.
- The documentation clearly treats the journal as part of quest runtime state management.

**Gap / unsupported claim**
- I did not find documented support for a true concurrency model in the reviewed source vocabulary.
- If the roadmap or docs imply concurrent journal mutation, locking, multi-writer coordination, or thread-safe progression, that language is not grounded in the current audit set.

**Current vs. target**
- Current: journal updates and runtime sequencing.
- Target: concurrency-aware journal handling, if intended by the roadmap.
- The safest wording is to describe the current system as ordered/sequenced rather than concurrent.

---

### Phase 12: branching quest chains

**Verdict: partial**

**Evidence supporting current coverage**
- `docs/quests/quest_branching_examples.md` exists and provides concrete branching examples.
- The phase-18 architecture/runtime docs keep branching in the quest-framework vocabulary, but the reviewed source set does not expose a dedicated branching API surface.

**Mismatch / overclaim risk**
- Branching is currently documented as a **pattern** or **target approach**, not as a stable callable API.
- Any phrasing that presents branching quest chains as already available in `src/quests/quest_runtime.py` or `build/build_quests.py` would overstate the current implementation.

**Current vs. target**
- Current: branching examples and design patterns.
- Target: a first-class branching quest-chain model.
- The docs should keep that distinction explicit.

## Cross-phase mismatches and terminology drift

1. **“Compiler integration” needs a build-time qualifier**
   - Supported by `docs/quests/quest_build_pipeline.md` and `build/build_quests.py`.
   - Risk: wording can drift into implying a general compiler runtime API.

2. **“Battle-integrated quest actions” should stay tied to mission/event seams**
   - Supported by `docs/quests/runtime_event_audit.md` and the Jotnar clan arena mission example.
   - Risk: wording can drift into implying a standalone action subsystem.

3. **“Concurrency” is not currently evidenced**
   - The reviewed runtime docs support journal handling, but not concurrency primitives or coordination semantics.
   - Risk: overclaiming thread safety or multi-writer support.

4. **“Branching” is target-pattern language, not current API language**
   - `docs/quests/quest_branching_examples.md` should be treated as design guidance.
   - Risk: readers may infer a callable runtime surface that does not exist in the current source vocabulary.

## Smallest doc fixes to close the gaps

1. **`docs/quests/quest_branching_examples.md`**
   - Add an explicit “target pattern, not current API” note near the top.
   - Use phrasing that matches the current source vocabulary and avoids implying a callable branching surface.

2. **`docs/quests/quest_runtime_api.md`**
   - Clarify that journal behavior is sequenced through the quest runtime.
   - Avoid concurrency language unless it is explicitly documented as target-state only.

3. **`docs/quests/quest_build_pipeline.md`**
   - Keep the language anchored to build-time lowering and legacy compiler output.
   - Make it explicit that this is a build pipeline, not a new runtime compiler API.

4. **`docs/quests/runtime_event_audit.md`**
   - Keep the battle/mission mapping concrete and event-driven.
   - If the text implies more than hook-based integration, narrow it to the current seam vocabulary.

5. **`docs/quests/quest_framework_master_plan.md`**
   - Mark phases 9-12 more clearly as a mix of current implementation and target-state roadmap items.
   - Add a short note that phases 10-12 are not all equally mature in the current docs/source vocabulary.

## Bottom line

- **Phase 9** is documented well enough to pass, provided the language stays anchored to the build pipeline.
- **Phases 10-12** are only partially covered and need clearer current-vs-target labels.
- The biggest overclaim risk is **branching** being read as a current API and **concurrency** being read as implemented behavior.