# Quest build pipeline

**Status:** current implementation, with build-time verification only.  
This document describes what `build/build_quests.py` and `.\build_module.bat --no-cache` do in the current implementation. It does **not** describe a runtime test harness, a gameplay diagnostics suite, or a separate editor tool.

## Scope

The quest build pipeline is the build-time path that turns the quest source tree into the legacy compiler shape used by the Warband module build. It is intentionally narrow:

- it collects quest fragments from `src/quests/`
- it lowers schema-backed fragments into the legacy tuple output expected by the compiler path
- it combines those lowered fragments with legacy tuple fragments already present in source
- it performs build-time verification on the assembled quest data
- it emits generated build artifacts for the downstream module build

This is compile-time verification, not runtime verification.

## What `build/build_quests.py` does in the current implementation

In the audited source, `build/build_quests.py` is the build orchestrator for quest content. Its responsibility is to:

1. collect the quest fragments that the build pipeline knows about
2. lower schema-backed fragments into the legacy compiler output shape
3. preserve compatibility with existing tuple fragments
4. check the assembled output for build-time problems such as duplicate identifiers
5. hand the lowered data to the rest of the build flow

That is the current implementation. The script is not a gameplay simulator, does not execute quest logic in-engine, and does not replace runtime validation.

## What the pipeline does not do

The quest build pipeline does **not**:

- run the game
- run mission, dialogue, or battle scenes
- provide a separate diagnostics product
- act as a general-purpose validation framework outside the build step
- replace manual review of migration changes
- guarantee that every target-state pattern is already implemented

When this document uses target-oriented language elsewhere, it is describing roadmap intent, not a claim about the current implementation.

## Build-time verification command

Use the documented module build command for verification:

```bat
.\build_module.bat --no-cache
```

That command is the documented build-time verification entry point for the quest pipeline. It exercises the build path without relying on cached output.

## Generated reports and artifacts

Files under `docs/reports/*` are generated artifacts. They are useful for inspection, but they are **not** the source of truth for quest architecture, runtime behavior, or migration policy.

Treat the source files and quest docs as authoritative, and treat report output as build artifacts only.

## Build outputs and terminology

The pipeline is built around the compatibility-lowering path used by the current implementation. In documentation, keep these terms distinct:

- **current implementation**: the source-backed build behavior that exists now
- **build-time verification**: checks performed by `build/build_quests.py` and `.\build_module.bat --no-cache`
- **target-state**: future behavior that the docs describe as a roadmap item only
- **not yet implemented**: a capability that is documented but not present in the audited source

For migration and authoring guidance, see:

- [quest_migration_checklist.md](quest_migration_checklist.md)
- [quest_framework_overview.md](quest_framework_overview.md)
- [quest_framework_master_plan.md](quest_framework_master_plan.md)