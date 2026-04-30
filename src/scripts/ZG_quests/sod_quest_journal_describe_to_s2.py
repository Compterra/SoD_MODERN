from header_common import *
from header_operations import *
from src.constants.module_constants import *


def _append_line(text):
    return [
        (str_store_string, s0, text),
        (str_store_string, s2, "@{s2}{s0}^"),
    ]


def _append_heading(text):
    return _append_line(text) + _append_line("@------------------------------")


def _append_journal_entry(prefix, include_archive_day=False):
    lines = [
        (str_store_string, s1, "@    [{prefix}] "),
        (str_store_quest_name, s0, ":quest_no"),
        (str_store_string, s2, "@{s2}{s1}{s0}^"),
        (quest_get_slot, reg0, ":quest_no", slot_quest_sod_runtime_stage),
        (quest_get_slot, reg1, ":quest_no", slot_quest_sod_journal_chain_progress),
        (quest_get_slot, reg2, ":quest_no", slot_quest_sod_runtime_state),
    ]
    if include_archive_day:
        lines += [
            (quest_get_slot, reg3, ":quest_no", slot_quest_sod_journal_archive_day),
            (str_store_string, s0, "@        Stage {reg0} | Chain {reg1} | State {reg2} | Archived day {reg3}"),
            (str_store_string, s2, "@{s2}{s0}^"),
        ]
    else:
        lines += [
            (str_store_string, s0, "@        Stage {reg0} | Chain {reg1} | State {reg2}"),
            (str_store_string, s2, "@{s2}{s0}^"),
        ]
    return lines


def _append_journal_section(category, prefix, empty_message, include_archive_day=False):
    return [
        (assign, reg7, 0),
        (try_for_range, ":quest_no", all_quests_begin, all_quests_end),
            (quest_get_slot, ":journal_category", ":quest_no", slot_quest_sod_journal_category),
            (try_begin),
                (eq, ":journal_category", category),
                (assign, reg7, 1),
            ] + _append_journal_entry(prefix, include_archive_day) + [
            (try_end),
        (try_end),
        (try_begin),
            (eq, reg7, 0),
            (str_store_string, s0, empty_message),
            (str_store_string, s2, "@{s2}{s0}^"),
        (try_end),
    ]


script_sod_quest_journal_describe_to_s2 = [
    (call_script, "script_sod_quest_journal_update"),
    (str_clear, s2),
]

script_sod_quest_journal_describe_to_s2 += _append_line("@Quest Journal")
script_sod_quest_journal_describe_to_s2 += _append_line("@A live summary of the active log, priority markers, stage progress, chain progress, and archived reports.")
script_sod_quest_journal_describe_to_s2 += _append_line("@Legend: [PINNED] priority target | [MAIN] main line | [SIDE] optional work | [URGENT] time-sensitive")
script_sod_quest_journal_describe_to_s2 += _append_line("@")
script_sod_quest_journal_describe_to_s2 += _append_line("@Summary:")
script_sod_quest_journal_describe_to_s2 += [
    (assign, reg0, "$sod_quest_journal_active_count"),
    (assign, reg1, "$sod_quest_journal_pinned_count"),
    (assign, reg2, "$sod_quest_journal_main_count"),
    (assign, reg3, "$sod_quest_journal_side_count"),
    (assign, reg4, "$sod_quest_journal_urgent_count"),
    (assign, reg5, "$sod_quest_journal_completed_count"),
    (assign, reg6, "$sod_quest_journal_failed_count"),
    (assign, reg9, "$sod_quest_journal_expiring_count"),
    (assign, reg10, "$sod_quest_journal_capacity"),
]
script_sod_quest_journal_describe_to_s2 += _append_line("@Tracked quests: {reg0}/{reg10} | Pinned: {reg1} | Main: {reg2} | Side: {reg3} | Urgent: {reg4} | Expiring: {reg9} | Completed: {reg5} | Failed: {reg6}")
script_sod_quest_journal_describe_to_s2 += _append_line("@")

script_sod_quest_journal_describe_to_s2 += _append_heading("@Active Quests")
script_sod_quest_journal_describe_to_s2 += _append_journal_section(
    sod_quest_journal_category_active,
    "ACTIVE",
    "@    No active quests are currently tracked in the journal.",
)
script_sod_quest_journal_describe_to_s2 += _append_line("@")

script_sod_quest_journal_describe_to_s2 += _append_heading("@Completed Archive")
script_sod_quest_journal_describe_to_s2 += _append_journal_section(
    sod_quest_journal_category_completed,
    "DONE",
    "@    No completed quests have been archived yet.",
    include_archive_day=True,
)
script_sod_quest_journal_describe_to_s2 += _append_line("@")

script_sod_quest_journal_describe_to_s2 += _append_heading("@Failed Archive")
script_sod_quest_journal_describe_to_s2 += _append_journal_section(
    sod_quest_journal_category_failed,
    "FAILED",
    "@    No failed quests have been archived yet.",
    include_archive_day=True,
)
script_sod_quest_journal_describe_to_s2 += _append_line("@")
script_sod_quest_journal_describe_to_s2 += _append_line("@End of journal.")

script_sod_quest_journal_describe_to_s2 = script_sod_quest_journal_describe_to_s2
SCRIPT = script_sod_quest_journal_describe_to_s2
SCRIPTS = [("sod_quest_journal_describe_to_s2", script_sod_quest_journal_describe_to_s2)]
