# Quest framework overview

This page is the entry point for the quest documentation set. It helps readers distinguish the **current implementation** from **target-state** roadmap content and shows how the phase-18 reference package fits together.

## Label convention

Use these labels consistently when reading the quest docs:

- **current implementation**: backed by audited source in `src/quests/` or `build/`
- **target-state**: roadmap language, design targets, or planned extensions that are not yet implemented
- **build-time verification**: checks performed by `build/build_quests.py` and `.\build_module.bat --no-cache`
- **not yet implemented**: wording used when the source does not currently prove the feature exists

## Start here

If you want the roadmap first, read:

- [quest_framework_master_plan.md](quest_framework_master_plan.md)

If you want the consolidated phase-18 reference package, read the linked docs below as a set:

- [quest_framework_architecture.md](quest_framework_architecture.md)
- [quest_runtime_api.md](quest_runtime_api.md)
- [quest_authoring_guide.md](quest_authoring_guide.md)
- [quest_content_examples.md](quest_content_examples.md)
- [quest_branching_examples.md](quest_branching_examples.md)
- [quest_migration_checklist.md](quest_migration_checklist.md)
- [quest_build_pipeline.md](quest_build_pipeline.md)
- [quest_dynamic_generation_rules.md](quest_dynamic_generation_rules.md)

The phase-18 pages are intended to be read as one navigable package rather than isolated notes.

## How the roadmap phases read in the current docs

The docs intentionally separate audited current behavior from roadmap material:

- **Phase 1** — audit baseline and terminology check
- **Phases 2-4** — architecture, runtime API, and event seams grounded in the current implementation
- **Phases 5-6** — storage and generation guidance, with target-state language where appropriate
- **Phases 7-8** — authoring helpers and examples, with build-time verification boundaries
- **Phases 9, 10, 11, 12** — branching, journal, battle, and related patterns; keep target-state wording where the source does not prove a unified API
- **Phase 15** — migration checklist and compatibility-first sequencing
- **Phase 16** — build pipeline description and build-time verification
- **Phase 17** — verification-oriented documentation tied to the build path, not a separate test framework
- **Phase 18** — consolidation, navigation, and documentation packaging

Read those phases using the label convention above so current implementation, partial coverage, and target-state content stay separate.

## Phase-18 reference package

The phase-18 package is the normalized documentation set for the quest framework.

### Architecture and runtime

- [quest_framework_architecture.md](quest_framework_architecture.md)
- [quest_runtime_api.md](quest_runtime_api.md)

### Authoring and examples

- [quest_authoring_guide.md](quest_authoring_guide.md)
- [quest_content_examples.md](quest_content_examples.md)
- [quest_branching_examples.md](quest_branching_examples.md)

### Migration, build, and generation

- [quest_migration_checklist.md](quest_migration_checklist.md)
- [quest_build_pipeline.md](quest_build_pipeline.md)
- [quest_dynamic_generation_rules.md](quest_dynamic_generation_rules.md)

## Reader paths

- To understand the source-backed model first, start with the architecture and runtime pages.
- To work on content migration, read the migration checklist and build pipeline together.
- To author quest content, read the authoring guide and content examples together.
- To evaluate roadmap wording, read the master plan alongside the target-state pages.

The master plan links here, and this page links back to the master plan, so the documentation set stays navigable in both directions.