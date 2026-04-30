# Phase 11 Quest Journal

## Overview

Phase 11 adds a player-facing quest journal layer on top of the existing quest runtime. The journal still preserves the core runtime lifecycle (`runtimes` and `archived_runtimes`) and event dispatch behavior, but now also exposes capacity rules, pinning, classification, sorting, filtering, progress summaries, and warning flags that are suitable for UI consumption.

The canonical journal/runtime surface for this phase is:

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
- `QuestRuntime.quest_category()`
- `QuestRuntime.quest_priority()`
- `QuestRuntime.warning_flags()`
- `QuestRuntime.progress_summary()`
- `QuestRuntime.journal_snapshot()`

## Journal data model

`QuestJournal` remains the owner of active and archived quest runtimes:

- `runtimes` contains active runtimes.
- `archived_runtimes` contains runtimes that have been completed, failed, or otherwise removed from the active set.
- `journal_snapshot()` returns a plain dictionary that groups active and archived quests into a UI-friendly shape.

The journal also tracks classification and state groupings using quest id sets:

- `pinned_quest_ids`
- `main_quest_ids`
- `side_quest_ids`
- `urgent_quest_ids`
- `completed_quest_ids`
- `failed_quest_ids`

These groupings are derived from runtime metadata and journal operations. They are intended to be deterministic and easy to serialize.

## Active quest capacity and pinning

`QuestJournal.max_active_quests` sets the capacity limit for non-pinned active quests.

Capacity rules:

- The limit applies only to non-pinned active quests.
- Pinned quests may stay active even when the limit has been reached.
- `can_register_runtime()` should return `False` when a non-pinned runtime would exceed the current capacity.
- `register_runtime(..., allow_overflow=False)` must raise `RuntimeError` with a clear message if a non-pinned runtime would exceed the limit.
- Passing `allow_overflow=True` allows registration to proceed even when the capacity check would otherwise fail.

Pinning rules:

- `pin_runtime()` marks a runtime as pinned and records the quest id in `pinned_quest_ids`.
- `unpin_runtime()` removes the pinned state and removes the quest id from `pinned_quest_ids`.
- Pinned quests should be favored in journal ordering and should bypass capacity pressure.

## Classification

Classification is duck-typed. The journal may derive category, priority, and state flags from runtime or quest metadata keys such as:

- `category`
- `quest_category`
- `quest_line`
- `pinned`
- `main`
- `side`
- `urgent`
- `priority`
- `expires_in_days`
- `expires_at`
- `warning_threshold`
- `failure_threshold`
- `chain_id`
- `chain_index`
- `chain_length`
- `stage_index`
- `stage_count`
- `stage_progress`

Canonical category buckets are:

- `main`
- `side`
- `urgent`
- `misc`

The helper methods expose the normalized view:

- `QuestRuntime.quest_category()` returns the normalized category string.
- `QuestRuntime.quest_priority()` returns the numeric priority used by journal ordering.
- `QuestRuntime.is_main_quest()`, `QuestRuntime.is_side_quest()`, and `QuestRuntime.is_urgent_quest()` provide convenience checks.
- `QuestRuntime.is_pinned()` reports the pinned state.

`misc` is the fallback category when a quest does not clearly map to main, side, or urgent.

## Sorting and filtering

`QuestJournal.sorted_active_runtimes()` is the canonical ordering helper for active quests.

The ordering is deterministic and should prioritize, in order:

1. pinned quests
2. urgent quests
3. main quests
4. higher numeric priority
5. better stage/chain progress
6. quest id as the final tie-breaker

`filtered_active_runtimes()` provides the journal’s runtime filter helper and should support category, pinned, and urgent filters. `active_runtime_ids()` returns the corresponding ids, optionally sorted.

The journal snapshot should use `sorted_active_runtimes()` for its active quest listing so UI consumers get a stable, predictable order.

## Progress summaries and warning flags

`QuestRuntime.progress_summary()` returns a plain dictionary for UI and QA consumers. It must include:

- `quest_id`
- `title`
- `category`
- `priority`
- `pinned`
- `urgent`
- `status`
- `stage_progress`
- `chain_progress`
- `warnings`

The progress summary is intentionally snapshot-oriented. It should summarize stage progress and chain progress without requiring the caller to inspect internal runtime objects.

`QuestRuntime.warning_flags()` returns canonical warning labels. The documented warning strings are:

- `expiration_warning`
- `failure_warning`

Warning flags may be empty when no warning applies.

`QuestRuntime.journal_snapshot()` returns the per-runtime snapshot used by the journal. It should remain a plain dictionary and be suitable for nested inclusion inside `QuestJournal.journal_snapshot()`.

## Completed and failed archives

`QuestJournal.complete_runtime()` and `QuestJournal.fail_runtime()` archive terminal outcomes while preserving the runtime record.

Behavior requirements:

- `complete_runtime()` must set `metadata['outcome'] = 'completed'` before archiving.
- `fail_runtime()` must set `metadata['outcome'] = 'failed'` before archiving.
- Completed quest ids are tracked in `completed_quest_ids`.
- Failed quest ids are tracked in `failed_quest_ids`.
- Archived runtimes remain accessible through `archived_runtimes`.

These outcome helpers should not change the existing dispatch model. They only add journal-level lifecycle tracking on top of the runtime archive flow.

## Journal snapshot shape

`QuestJournal.journal_snapshot()` must include these top-level keys:

- `active_quest_ids`
- `archived_quest_ids`
- `completed_quest_ids`
- `failed_quest_ids`
- `pinned_quest_ids`
- `main_quest_ids`
- `side_quest_ids`
- `urgent_quest_ids`
- `active_count`
- `capacity_limit`
- `capacity_remaining`
- `quests`

The `quests` collection should be plain data, not live runtime objects, and should align with the canonical active ordering.

## Implementation notes

- The journal layer is duck-typed and should tolerate minimal quest stub objects.
- The API should prefer plain dict snapshots over custom wrapper classes for testability.
- Classification and warnings are derived from metadata when explicit runtime flags are absent.
- The journal layer does not replace the runtime event system; it provides a richer management and inspection surface on top of it.