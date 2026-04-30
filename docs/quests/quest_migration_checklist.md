# Quest migration checklist

**Status:** compatibility-first migration guidance for the current implementation.  
This checklist describes how to move quest content toward the schema-backed path without breaking the legacy tuple export shape.

## Core compatibility rule

Preserve the exact compatibility export shape:

```python
QUESTS = [*quest_chain(...).as_legacy_tuples()]
```

That export shape is the current implementation boundary between schema-backed fragments and the legacy compiler output. Migration work must keep that shape intact until the build-time verification path proves the translated content is stable.

## Migration sequence

Use the following order. Do not skip steps.

1. **Inventory**
   - List the legacy tuple fragments and the schema-backed fragments involved in the quest area being migrated.
   - Identify any shared identifiers, shared storage, or shared event hooks that could be affected.

2. **Translate**
   - Convert the target content into schema-backed helpers and fragments where appropriate.
   - Keep the compatibility-lowering path exact.
   - Do not remove the legacy tuple form until the translated path has been validated.

3. **Validate**
   - Run build-time verification through `build/build_quests.py` and `.\build_module.bat --no-cache`.
   - Confirm that the lowered output still matches the expected legacy compiler shape.

4. **Compare**
   - Compare the generated output against the legacy baseline.
   - Check for duplicate identifiers, missing fragments, changed hook coverage, or unexpected lowering changes.

5. **Retire legacy wording**
   - Once validation and comparison pass, update the documentation and in-source wording to reflect the schema-backed path.
   - Retire only the legacy phrasing that has been proven unnecessary.

## Rollback and review

If validation fails, stop the migration and review the change before continuing.

Rollback means:

- keep the previous working export shape
- revert any partially translated fragment that breaks build-time verification
- inspect the lowered output before attempting another migration step

Do **not** treat migration as one-pass automation. The current implementation still depends on compatibility-first sequencing and manual review.

## What stays visible during migration

Keep these points explicit in the code and docs:

- the legacy compiler shape remains the authoritative export boundary
- schema-backed fragments are lowered into that shape
- build-time verification is the checkpoint for each migration step
- target-state wording stays target-state until the source proves it is current implementation

## Current implementation vs target-state

Use these labels consistently:

- **current implementation**: the compatibility-lowering path and existing legacy export shape
- **target-state**: future helper expansions, future authoring shortcuts, or broader automation that is not yet implemented
- **build-time verification**: the comparison step used to confirm the migration is still compatible
- **not yet implemented**: any branch, helper, or automation that the source does not currently provide

For build details, see [quest_build_pipeline.md](quest_build_pipeline.md). For navigation across the full docs set, see [quest_framework_overview.md](quest_framework_overview.md).