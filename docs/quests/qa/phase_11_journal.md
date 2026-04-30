# Phase 11 QA Checklist: Quest Journal

Use this checklist to verify the journal and concurrency layer added in Phase 11.

## Scope

Validate the runtime and journal APIs:

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

Canonical warning strings:

- `expiration_warning`
- `failure_warning`

## Checklist

1. **Registration and archive transitions**
   - Register an active runtime successfully.
   - Confirm it appears in `runtimes`.
   - Complete or fail the runtime.
   - Confirm it moves to `archived_runtimes`.
   - Confirm the outcome is recorded in `metadata['outcome']`.

2. **Capacity enforcement**
   - Set `QuestJournal.max_active_quests` to a small limit.
   - Register non-pinned quests until the limit is reached.
   - Confirm an additional non-pinned registration is rejected by `can_register_runtime()`.
   - Confirm `register_runtime(..., allow_overflow=False)` raises `RuntimeError` with a clear message.

3. **Pinned quest bypass**
   - Pin a runtime with `pin_runtime()`.
   - Confirm the quest id is added to `pinned_quest_ids`.
   - Confirm a pinned runtime can remain active when the non-pinned capacity is full.
   - Confirm `unpin_runtime()` removes the pinned state.

4. **Classification**
   - Verify quests categorized through metadata are grouped correctly as:
     - `main`
     - `side`
     - `urgent`
     - `misc`
   - Confirm `main_quest_ids`, `side_quest_ids`, and `urgent_quest_ids` reflect the current active set.

5. **Sorting and filtering**
   - Confirm `sorted_active_runtimes()` places pinned quests first.
   - Confirm urgent quests sort ahead of non-urgent quests.
   - Confirm higher numeric priority sorts ahead of lower priority.
   - Confirm stage and chain progress affect ordering before quest id tie-breaks.
   - Confirm `filtered_active_runtimes()` respects category, pinned, and urgent filters.

6. **Progress summaries**
   - Confirm `QuestRuntime.progress_summary()` returns:
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
   - Confirm `stage_progress` and `chain_progress` are plain dicts.
   - Confirm the summary is suitable for a UI snapshot.

7. **Warning flags**
   - Confirm `QuestRuntime.warning_flags()` returns `expiration_warning` when the quest is near expiration.
   - Confirm `QuestRuntime.warning_flags()` returns `failure_warning` when the quest meets failure-warning conditions.
   - Confirm the warning list can be empty when no warning applies.

8. **Journal snapshot shape**
   - Confirm `journal_snapshot()` includes:
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
   - Confirm `quests` is plain snapshot data, not live runtime objects.
   - Confirm active ids follow the canonical sorted order.

## Expected outcome

The quest journal should behave like a deterministic manager for multiple concurrent quests while preserving the existing runtime and dispatch behavior.