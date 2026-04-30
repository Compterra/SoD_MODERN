try:
    from header_common import *  # noqa: F401,F403
    from header_operations import *  # noqa: F401,F403
except ImportError:
    pass

for _name, _default in (
    ("call_script", 0),
    ("jump_to_menu", 0),
    ("str_clear", 0),
):
    if _name not in globals():
        globals()[_name] = _default

try:
    menus
except NameError:
    menus = []

QUEST_JOURNAL_ROUTE_TOKEN = "mnu_quest_journal_report"
QUEST_JOURNAL_RETURN_MENU = "mnu_reports"


def _quest_journal_report_refresh():
    return [
        (call_script, "script_sod_quest_journal_update"),
        (call_script, "script_sod_quest_journal_describe_to_s2"),
        (call_script, "script_sod_quest_chain_describe_to_s2"),
        (call_script, "script_sod_quest_outcome_describe_to_s2"),
    ]


MENUS = [
    (
        "quest_journal_report",
        0,
        "{!}Quest Journal\n\n[ Active Log ]\n{s2}\n\n[ Chain Tracking ]\n{s3}\n\n[ Outcome Tracking ]\n{s4}\n\n[ Priority / Stage / Chain / Archive ]\nUse this record to review the current quest log, pinned priorities, stage progress, chain progress, expiration warnings, failure warnings, and archived entries.",
        "none",
        [],
        [
            ("quest_journal_report_back", [], "Back", [
                (call_script, "script_sod_quest_journal_update"),
                (call_script, "script_sod_quest_journal_describe_to_s2"),
                (call_script, "script_sod_quest_chain_describe_to_s2"),
                (call_script, "script_sod_quest_outcome_describe_to_s2"),
                (jump_to_menu, "mnu_reports"),
            ]),
        ],
    ),
]

menus += MENUS
