# Quest Runtime API

> Status: **current implementation** for the documented lifecycle terms below; this page does **not** claim a fully formalized state-machine API unless the source proves it.

This page describes the runtime vocabulary that is visible in the audited quest runtime and the way the documentation should read it.

## Scope note

- **current implementation**: runtime terms and outcomes already evidenced by `src/quests/quest_runtime.py`.
- **target-state**: any extra transition helpers, richer public APIs, or formal state-machine semantics that are not source-backed.
- **build-time verification**: not the runtime concern here; see [`quest_build_pipeline.md`](./quest_build_pipeline.md) for build-time lowering and verification.

Primary source anchors:

- [`src/quests/quest_runtime.py`](../../src/quests/quest_runtime.py)
- [`docs/quests/runtime_event_audit.md`](./runtime_event_audit.md)

## Runtime lifecycle terms

The runtime is best described as **lifecycle-oriented**. It has clear terms for handling hooks and for ending or advancing a quest, but the documentation should not imply a broader public state-machine API unless the audited source explicitly adds one.

| Runtime term | Current implementation outcome | What the term should mean in docs | Status |
| --- | --- | --- | --- |
| `handle_hook` | Receives an audited hook and processes it in the quest runtime context | The runtime entry point for hook handling | current implementation |
| `advance_stage` | Moves the quest forward to the next stage or equivalent progression step | Progression within the current quest lifecycle | current implementation |
| `complete` | Ends the quest with a terminal success outcome | Successful terminal lifecycle outcome | current implementation |
| `fail` | Ends the quest with a terminal failure outcome | Failed terminal lifecycle outcome | current implementation |
| `abort` | Ends the quest early without treating it as a normal success or failure path | Early termination or cancellation | current implementation |

## Lifecycle and transition summary

The current documentation should treat the runtime as a sequence of lifecycle outcomes rather than a fully generalized state machine.

| From | Runtime term | To / outcome | Notes |
| --- | --- | --- | --- |
| Active quest context | `handle_hook` | Hook processed in current context | The hook is handled, not reclassified as a new public API surface. |
| Active quest context | `advance_stage` | Next stage or equivalent progression step | This is the progression term the source-backed docs can rely on. |
| Active quest context | `complete` | Terminal success | No further progression is implied after completion. |
| Active quest context | `fail` | Terminal failure | No further progression is implied after failure. |
| Active quest context | `abort` | Terminal early stop | Use this term for cancellation-like endings. |

## What the runtime is not claiming

To keep the documentation aligned with the audited source, do not describe the runtime as if it already exposes:

- a generic transition graph API
- a formal event bus abstraction
- additional lifecycle methods beyond `handle_hook`, `advance_stage`, `complete`, `fail`, and `abort`
- a separate diagnostics subsystem

Those ideas belong in **target-state** language unless another source file explicitly proves them.

## How to read the runtime with the rest of the docs

- Use [`quest_framework_architecture.md`](./quest_framework_architecture.md) for the higher-level architecture and storage categories.
- Use [`runtime_event_audit.md`](./runtime_event_audit.md) for the audited seam list.
- Use [`quest_branching_examples.md`](./quest_branching_examples.md) for target-state branching patterns only.

When in doubt, prefer the term **current implementation** for source-backed runtime behavior and **target-state** for any broader lifecycle model.