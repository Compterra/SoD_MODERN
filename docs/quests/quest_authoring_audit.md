# Quest Authoring Audit

**Status:** current implementation audit  
**Scope:** schema-backed helpers, authoring helpers, compatibility lowering, and build-time verification  
**Not covered:** a standalone DSL, runtime diagnostics product, or a broader branching subsystem

This audit records what the current source supports today and where the documentation should stop making broader claims. The authored quest pipeline is currently based on schema-backed helpers that lower into the legacy tuple format during the build. It is not a separate language layer.

## Current implementation

The source-backed authoring path is:

1. Author quests with the schema-backed helpers in `src/quests/quest_schema.py`.
2. Export the compatibility shape expected by the legacy compiler:
   `QUESTS = [*quest_chain(...).as_legacy_tuples()]`
3. Run the build pipeline in `build/build_quests.py`, which performs build-time verification and compatibility lowering.

That path is the only implementation-backed claim this audit makes. Any broader authoring abstraction should be labeled **target-state** unless it is visible in the current source.

## What the audit confirms

### Schema-backed helpers are the current authoring surface

The current docs are strongest when they describe:

- schema-backed helpers
- authoring helpers
- compatibility lowering
- build-time verification

The docs are weaker when they say `DSL`, because that word suggests a separate language product or parser/runtime surface that the source does not currently prove.

### Validation is build-time only

`build/build_quests.py` provides build-time verification for the authored quest data. In the current implementation, validation belongs to the build pipeline, not to a standalone runtime diagnostics system.

That means the docs should say:

- build-time verification
- compile-time or build-time compatibility checks
- legacy tuple lowering checks

The docs should not imply:

- live runtime validation
- a separate diagnostics service
- an interactive editor validation loop

unless a source file explicitly adds that behavior later.

### Compatibility lowering is the bridge to legacy output

The current compatibility path is the important integration seam for authored quests. The build consumes the schema-backed fragments and emits legacy tuples for the existing Mount & Blade Warband quest pipeline.

The export shape that the docs should preserve exactly is:

```python
QUESTS = [*quest_chain(...).as_legacy_tuples()]
```

That shape is the documented compatibility contract, not a new runtime API.

## Current-vs-target wording guidance

### Current implementation language to keep

Use the following labels when the statement is source-backed:

- **current implementation**
- **build-time verification**
- **compatibility lowering**
- **schema-backed helpers**
- **authoring helpers**
- **audited seam**

### Target-state language to reserve for future work

Use **target-state** when the text discusses any of the following unless the current source proves them:

- branching helpers beyond the current documented surface
- richer authoring abstractions
- future helper expansions
- broader validation or diagnostics features
- additional tooling beyond the current documentation and build pipeline

## Branching and helper expansion status

Branching is documented as an important authoring concern, but it should be treated as **target-state** unless the current source explicitly exposes a branching helper or lowering rule for it.

Likewise, any future helper expansions should be written as planned compatibility work, not as already implemented behavior.

Examples of safe wording:

- “The roadmap expects future branching helpers to lower into the same compatibility export shape.”
- “A target-state helper expansion could reduce boilerplate.”
- “The current implementation does not yet expose that helper.”

Examples of wording to avoid:

- “The DSL supports branching.”
- “The authoring system provides diagnostics.”
- “The runtime validates authored content.”
- “The helper surface is fully formalized.”

## Audit conclusion

The current source supports a narrow, practical authoring path:

- schema-backed helpers for authored quest content
- compatibility lowering to legacy tuples
- build-time verification in the build pipeline

That is enough to document the current implementation accurately. Anything broader should be labeled **target-state** and kept separate from source-backed claims.

## Related documentation

- [Quest Authoring Guide](./quest_authoring_guide.md)
- [Quest Content Examples](./quest_content_examples.md)
- [Quest Framework Overview](./quest_framework_overview.md)