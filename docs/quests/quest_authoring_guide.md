# Quest Authoring Guide

**Current implementation:** authoring uses schema-backed helpers that lower into legacy tuples at build time.  
**Target-state:** any richer helper expansion, branching convenience layer, or editor integration that is not already present in source.

## Scope note

In this guide, **tooling** means the documentation set, schema-backed helpers, examples, and migration guidance that support quest authoring.

It does **not** mean:

- a standalone editor
- a new runtime API
- a separate DSL runtime
- a broader diagnostics product

If a feature is not backed by the current source, treat it as **target-state**.

## What authors write today

The current authoring model is intentionally narrow:

- use the schema-backed helpers defined in `src/quests/quest_schema.py`
- express quest content in the documented helper format
- keep the compatibility export shape intact:
  `QUESTS = [*quest_chain(...).as_legacy_tuples()]`
- let `build/build_quests.py` perform build-time verification and compatibility lowering

That is the current implementation. The guide should not imply a separate language layer.

## Authoring workflow

### 1. Define quest content with schema-backed helpers

Use the documented authoring helpers to describe quest content in a structured way. The current docs should describe those helpers as helper-based authoring, not as a DSL.

### 2. Preserve the compatibility export

The legacy compiler path still expects the lowered tuple output. The export shape should remain exactly:

```python
QUESTS = [*quest_chain(...).as_legacy_tuples()]
```

### 3. Run build-time verification

Validation happens during the build pipeline. The guide should say **build-time verification** or **compile-time verification** when referring to validation that the build system performs.

## What the build checks

The current build-time verification is the right place to describe:

- compatibility lowering from schema-backed fragments to legacy tuples
- structural checks that the authored data can be emitted cleanly
- duplicate or invalid content handling when the build pipeline detects it

Do not describe this as a runtime diagnostics system. The current source supports build-time verification only.

## Current-vs-target wording

Use the following labels consistently:

- **current implementation**: source-backed helper behavior that exists now
- **target-state**: roadmap material or future helper expansion
- **build-time verification**: checks performed in the build pipeline
- **not yet implemented**: anything the source does not currently provide

### Target-state examples

These are acceptable only as future-facing guidance:

- future helper simplification for repetitive quest patterns
- planned branching convenience helpers
- migration advice that depends on helper expansion not yet present in source

When you mention those items, make the target-state status explicit.

## Migration guidance

Migration guidance should be written as a compatibility path, not as a promise of a complete one-pass conversion tool.

A safe migration sequence is:

1. inventory the current quest fragments
2. translate legacy patterns into schema-backed helpers
3. validate through the build pipeline
4. compare the lowered tuples with the expected legacy output
5. retire the old wording only after build-time verification passes

If a step depends on a future helper or future branching convenience, label it **target-state**.

## Examples of wording to prefer

- “schema-backed helpers”
- “authoring helpers”
- “compatibility lowering”
- “build-time verification”
- “target-state branching support”
- “not yet implemented”

## Wording to avoid

- “the DSL”
- “runtime diagnostics”
- “standalone authoring system”
- “fully formalized branching API”
- “interactive validation engine”

## Related documentation

- [Quest Authoring Audit](./quest_authoring_audit.md)
- [Quest Content Examples](./quest_content_examples.md)
- [Quest Framework Overview](./quest_framework_overview.md)