# QA Report: Phases 13-15

Scope: `phase 13 rewards/consequences`, `phase 14 narrative/dialogue integration`, `phase 15 content migration strategy`

Reviewed sources:
- `docs/quests/quest_framework_master_plan.md`
- `docs/quests/quest_state_storage_audit.md`
- `docs/quests/runtime_event_audit.md`
- `docs/quests/quest_authoring_audit.md`
- `docs/quests/quest_authoring_guide.md`
- `docs/quests/quest_migration_checklist.md`
- `docs/quests/quest_framework_overview.md`
- `src/quests/quest_runtime.py`
- `src/quests/quest_schema.py`

## Verdict summary

| Phase | Verdict | Current/target state | QA note |
| --- | --- | --- | --- |
| Phase 13 rewards/consequences | partial | mixed | The docs support quest-state terminal handling and journal updates, but they do not evidence a general reward/consequence system beyond quest state, mirrors, and cleanup. |
| Phase 14 narrative/dialogue integration | partial | mixed | The docs support event seams for dialogue and mission triggers, but they do not define a dedicated narrative layer or a new dialogue API. |
| Phase 15 content migration strategy | partial | mixed, mostly target-state | The migration guidance exists, but it needs tighter sequencing, rollback language, and clearer current-vs-target labeling. |

## Phase 13: rewards/consequences

### What is supported

The current documentation and runtime vocabulary support the following quest outcomes:

- terminal quest-state transitions in `src/quests/quest_runtime.py`
- quest journal updates in the runtime layer
- quest-state cleanup and mirror rules in `docs/quests/quest_state_storage_audit.md`
- event-driven state changes where quest logic reacts to runtime signals rather than a separate reward engine

That is enough to describe **quest consequences** in the narrow sense of:
- quest completion/failure state
- journal/log updates
- cleanup of quest state mirrors

### What is not supported

The current audited sources do **not** justify language that implies a broader reward system, such as:

- a general reward API
- inventory or economy payouts as a documented quest framework feature
- reputation/faction/relationship mutation as part of the quest framework contract
- any persistent consequence model that is not already grounded in quest state or journal state

### QA verdict

This phase is **partial** because the docs cover the terminal quest-state side of the story, but the phrase `rewards/consequences` is broader than what the runtime/storage model currently documents.

### Smallest doc fixes needed

1. In `docs/quests/quest_framework_master_plan.md`, label phase 13 language as **current quest-state consequences** vs **future broader reward systems**.
2. In `docs/quests/quest_authoring_guide.md`, scope consequence wording to quest state, journal updates, and cleanup unless a specific behavior is already documented elsewhere.
3. In `docs/quests/quest_state_storage_audit.md`, add a short note that the audited state model does not define a general reward subsystem.

## Phase 14: narrative/dialogue integration

### What is supported

The current documentation does support integration points between quests and runtime events:

- `docs/quests/runtime_event_audit.md` maps quest triggers to dialogue/mission/runtime seams
- `docs/quests/quest_framework_overview.md` routes readers toward runtime-oriented quest documentation
- `src/quests/quest_runtime.py` provides the runtime vocabulary for state changes that can be driven by events

This is enough to say that quest logic can respond to dialogue-related events.

### What is not supported

The documentation does **not** establish:

- a dedicated narrative subsystem inside the quest framework
- a new authored dialogue API
- a full narrative branching layer that is currently implemented in the source
- any claim that dialogue integration is more than event-driven triggering and state response

The phrase `narrative/dialogue integration` is therefore too broad if it is read as a completed framework feature. In the current docs, it is better understood as **runtime event integration with dialogue-facing seams**.

### QA verdict

This phase is **partial** because the docs show integration seams, but they do not justify a separate narrative system or a richer dialogue API.

### Smallest doc fixes needed

1. In `docs/quests/runtime_event_audit.md`, explicitly say that the current scope is **event seams**, not a narrative subsystem.
2. In `docs/quests/quest_authoring_guide.md`, keep dialogue-related examples framed as **quest triggers and state reactions**, not as a standalone dialogue authoring surface.
3. In `docs/quests/quest_framework_master_plan.md`, mark any narrative language in phase 14 as roadmap intent unless it is backed by the runtime audit.

## Phase 15: content migration strategy

### What is supported

The documentation set does provide migration-oriented material:

- `docs/quests/quest_authoring_audit.md` discusses compatibility and migration pressure
- `docs/quests/quest_authoring_guide.md` gives author-facing migration language
- `docs/quests/quest_migration_checklist.md` provides actionable migration steps and exit criteria
- `src/quests/quest_schema.py` grounds the current schema-backed fragment vocabulary

This is enough to support a migration strategy discussion at the documentation level.

### What is not supported or needs tightening

The migration guidance still reads as mixed state because it does not clearly separate:

- what is already supported by the current schema-backed fragments
- what is still a transition target for legacy tuple fragments
- what should happen if migration validation fails
- what order authors should follow when migrating content

The main gaps are:

- sequencing is implied, but not stated as an explicit order
- rollback language is missing or too light
- exit criteria are present in spirit, but not consistently tied to a validation step
- the docs do not always distinguish current implementation from roadmap target-state wording

### QA verdict

This phase is **partial** because the docs provide real migration guidance, but the guidance is not yet specific enough to be treated as fully trustworthy operational procedure.

### Smallest doc fixes needed

1. In `docs/quests/quest_migration_checklist.md`, add an explicit migration sequence such as:
   - inventory legacy content
   - translate into schema-backed fragments
   - validate against the build pipeline
   - review generated output
   - only then retire legacy wording
2. Add a short rollback note that says migration should stop and be reviewed if validation fails.
3. In `docs/quests/quest_authoring_guide.md`, label any future-facing migration advice as target-state unless it is already supported by the current schema/runtime vocabulary.
4. In `docs/quests/quest_authoring_audit.md`, keep the compatibility discussion tightly tied to the existing fragment model so readers do not infer a larger automated conversion system than actually exists.

## Cross-phase terminology drift

The main terminology risk across phases 13-15 is that the docs sometimes use broad roadmap language where the current source only supports narrower quest-framework behavior.

### Terms that should stay narrow
- `rewards/consequences` should map to quest-state transitions, journal updates, and cleanup unless a broader effect is explicitly documented
- `narrative/dialogue integration` should mean event seams and state reactions, not a standalone narrative engine
- `content migration strategy` should mean documented translation and validation steps, not a fully automated conversion pipeline

### Terms that should be labeled as target-state when used
- any reward or consequence beyond quest state/journal behavior
- any dialogue or narrative capability beyond event-triggered quest logic
- any migration workflow that assumes one-pass automation or safe rollback without an explicit documented step

## Recommended minimal edits

If the goal is to close the gaps with the smallest doc change set, the parent agent should update only the wording and labels in these files:

- `docs/quests/quest_framework_master_plan.md`
- `docs/quests/quest_authoring_guide.md`
- `docs/quests/quest_migration_checklist.md`
- `docs/quests/runtime_event_audit.md`
- `docs/quests/quest_state_storage_audit.md`

No new APIs or implementation work are required by this QA pass; the issue is scope control and terminology precision.