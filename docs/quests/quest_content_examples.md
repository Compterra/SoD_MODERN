# Quest Content Examples

**Current implementation:** these examples show authoring patterns built from schema-backed helpers and compatibility lowering.  
**Not a language claim:** the examples are not proof of a separate DSL or a runtime authoring system.

## Purpose of this page

This page collects illustrative quest-authoring shapes so authors can see how the current helper-based workflow fits together.

These examples are intentionally limited to:

- authoring patterns
- illustrative field shapes
- compatibility-lowering output
- build-time verification expectations

They are **not** a claim that the project has a separate language layer, a standalone editor, or a richer runtime diagnostics system.

## Preserve the compatibility export

The exact compatibility export shape remains:

```python
QUESTS = [*quest_chain(...).as_legacy_tuples()]
```

That shape is the current implementation contract for build-time lowering into legacy tuples.

## Example rules

When reading or writing examples on this page, keep these rules in mind:

- treat helper names as source-backed only when they appear in the current docs or source
- treat placeholders as illustrative, not callable API claims
- treat unexpanded sections as examples of structure, not as completed features
- keep branching and future helper expansion labeled **target-state** unless the current source explicitly proves them

## Example 1: simple helper-based quest shape

```python
QUESTS = [*quest_chain(
    # illustrative only: replace these placeholders with the real quest content
    # defined by the current authored quest
    ...
).as_legacy_tuples()]
```

This example shows the compatibility export shape only. The placeholder fields are illustrative and should not be read as proof of an extra runtime DSL.

## Example 2: schema-backed fragments lowered at build time

```python
quest_chain(
    # current implementation: schema-backed helpers describe the quest content
    # build/build_quests.py performs the lowering and build-time verification
    ...
).as_legacy_tuples()
```

This pattern is the current implementation path:

- author with schema-backed helpers
- keep the lowering path explicit
- verify the result during the build

## Example 3: future-facing branching pattern

```python
# target-state only: this is an illustrative branching shape
# if the source later adds a branching helper, it should still lower
# into the same compatibility export shape.
```

This example is intentionally non-executable. It documents a target-state idea only and must not be presented as an existing API.

## How to describe placeholders

Use this wording when a field or helper call is only meant to illustrate structure:

- **illustrative only**
- **placeholder**
- **target-state**
- **not yet implemented**

Avoid wording that makes the placeholder look like a callable runtime feature.

## What not to infer from examples

Do not infer from these examples that the project already has:

- a standalone DSL runtime
- interactive diagnostics
- a formal branching API beyond the current source
- any new authoring surface beyond schema-backed helpers and build-time verification

## Related documentation

- [Quest Authoring Audit](./quest_authoring_audit.md)
- [Quest Authoring Guide](./quest_authoring_guide.md)
- [Quest Framework Overview](./quest_framework_overview.md)