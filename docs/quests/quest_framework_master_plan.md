# Quest Framework Master Plan

## Purpose

This document tracks the quest framework rollout from the earliest runtime scaffolding through the Phase 11 journal layer. The goal is to keep the runtime, event system, giver runtime, schema layer, and player-facing journal aligned as one coherent system.

## Phase matrix

| Phase | Focus | Status | Notes |
| --- | --- | --- | --- |
| Phase 01 | Core quest domain and schema foundations | Complete | Base quest metadata, stage definitions, and typed shapes. |
| Phase 02 | Quest runtime scaffolding | Complete | Runtime objects and stage progression wiring. |
| Phase 03 | Event catalog and dispatch model | Complete | Quest events, subscriptions, and dispatcher behavior. |
| Phase 04 | Event sources and emitters | Complete | Runtime emitters and source adapters. |
| Phase 05 | Quest giver runtime | Complete | NPC-facing quest giver logic and handoff flow. |
| Phase 06 | Domain validation and template refinement | Complete | Quest templates, stages, and chain metadata tightened. |
| Phase 07 | Progress and state tracking | Complete | Runtime state summaries and stage tracking expanded. |
| Phase 08 | Archive and terminal lifecycle support | Complete | Active/archived runtime separation and terminal handling. |
| Phase 09 | Documentation and schema alignment | Complete | Contract language stabilized across runtime and docs. |
| Phase 10 | Runtime QA and event behavior verification | Complete | Existing runtime and dispatch coverage stabilized. |
| Phase 11 | Quest journal and concurrency layer | Complete | Capacity, pinning, classification, sorting, filtering, progress summaries, warning flags, and archive outcome tracking. |

## Completed architecture

The quest framework now supports:

- quest templates and stage metadata
- runtime progression and terminal outcomes
- event-driven updates
- NPC quest giver behavior
- active and archived runtime tracking
- player-facing journal summaries
- capacity management for concurrent active quests
- deterministic journal ordering and filtering

## Phase 11 summary

Phase 11 completes the journal layer that sits on top of the existing runtime system.

### Journal responsibilities

`QuestJournal` now acts as the central manager for the active quest list and the archived quest history. It preserves the existing `runtimes` and `archived_runtimes` collections while adding journal-level groupings and UI-oriented snapshots.

The canonical public surface for this phase is:

- `QuestJournal.max_active_quests`
- `QuestJournal.pinned_quest_ids`
- `QuestJournal.main_quest_ids`
- `QuestJournal.side_quest_ids`
- `QuestJournal.urgent_quest_ids`
- `QuestJournal.completed_quest_ids`
- `QuestJournal.failed_quest_ids`
- `QuestJournal.sorted_active_runtimes()`
- `QuestJournal.filtered_active_runtimes()`
- `QuestJournal.journal_snapshot()`
- `QuestJournal.complete_runtime()`
- `QuestJournal.fail_runtime()`

### Runtime journal helpers

`QuestRuntime` now exposes normalized journal helpers for classification, priority, warning, and progress inspection:

- `QuestRuntime.quest_category()`
- `QuestRuntime.quest_priority()`
- `QuestRuntime.warning_flags()`
- `QuestRuntime.progress_summary()`
- `QuestRuntime.journal_snapshot()`

### Behavior summary

- Active quest capacity applies to non-pinned quests only.
- Pinned quests may remain active even when the capacity limit has been reached.
- Sorting is deterministic and prioritizes pinned, urgent, main, higher priority, better progress, and quest id.
- Filtering supports category, pinned, and urgent views.
- Progress summaries and journal snapshots return plain dictionaries suitable for UI or testing.
- Completion and failure helpers set `metadata['outcome']` before archiving the runtime.

## Documentation alignment

The Phase 11 journal documentation and QA notes should remain consistent with the runtime contract and snapshot keys. If the runtime changes, the master plan should be updated in the same change set so the architecture report, QA checklist, and runtime behavior stay synchronized.

## Forward path

With Phase 11 complete, future work should focus on presentation and integration layers rather than changing the journal model itself. The core runtime and journal APIs are now stable enough for UI consumers to build on top of them.