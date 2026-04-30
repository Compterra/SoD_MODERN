# Quest Branching Examples

> Status: **target-state** examples only. This document is **not current API** documentation and should not be read as proof that a callable branching helper already exists in source.

This page collects branching patterns that are useful for authors and maintainers to reason about, but the patterns here are design targets unless the source explicitly proves otherwise.

## Scope note

- **current implementation**: the hybrid quest model, build lowering, and runtime lifecycle vocabulary already present in the source-backed docs.
- **target-state**: branching helpers, branch graph conveniences, or branching APIs that are not yet implemented.
- **not yet implemented**: anything described here as a planned extension or illustrative branch shape.
- **build-time verification**: the lowering path that still preserves the compatibility export shape.

The compatibility export path remains the same when content is lowered:

```python
QUESTS = [*quest_chain(...).as_legacy_tuples()]
```

That exact shape is the current build/export anchor. The branching patterns below are about how authors may want to structure content, not about adding new runtime methods.

## How to read these examples

Each example is labeled as a design target or planned extension.

- If the example describes a conditional path, treat it as **target-state** unless a source file already proves the helper exists.
- If the example mentions branch selection, treat it as an authoring pattern rather than a callable branching API.
- If the example looks like a helper call, read it as illustrative syntax only.

## Example 1: simple two-way branch

**Status: target-state / design target**

A quest may eventually offer a simple two-way choice:

- path A continues the current quest line
- path B diverts to an alternative resolution

This is useful as a documentation pattern, but it is **not yet implemented** as a public branching helper.

## Example 2: conditional branch gate

**Status: target-state / planned extension**

A conditional gate may eventually choose between one of several outcomes based on quest state, mirror state, or quest-giver memory.

Illustrative shape only:

- check current quest-owned state
- consult mirrored or remembered state if needed
- route to the next authored fragment

This example describes an authoring pattern, not a callable API claim.

## Example 3: branching with a fallback path

**Status: target-state / design target**

A fallback path is useful when authors want a quest to continue even if a preferred branch is unavailable.

Illustrative outcome:

- preferred branch is selected when the condition is met
- fallback branch is selected when the condition fails
- the quest still lowers through the same compatibility export shape

Again, this is a pattern for documentation and future authoring convenience, not a source-backed helper.

## Example 4: multi-step branch fan-out

**Status: target-state / not yet implemented**

A more elaborate branch fan-out may eventually route one quest into several mutually exclusive tracks.

Use this as a planning example only:

- one starting state
- several candidate branches
- a final authored path selected at runtime or build-time, depending on the future design

Do not read this as evidence of an existing branching DSL, runtime branch engine, or new transition helper.

## Practical guidance

When writing branching documentation elsewhere in this set:

- keep the phrase **current implementation** for the hybrid lowering path
- keep the phrase **target-state** for any branch logic that is not source-backed
- avoid implying a new branching API
- preserve the exact compatibility export shape shown above

For the runtime terms that support these patterns, see:

- [`quest_runtime_api.md`](./quest_runtime_api.md)

For the architecture and storage taxonomy, see:

- [`quest_framework_architecture.md`](./quest_framework_architecture.md)