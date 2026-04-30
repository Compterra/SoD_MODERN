from header_operations import *
from module_constants import *

SCRIPTS = [
    (
        "companion_report",
        [
            (store_script_param_1, ":troop_no"),
            (try_begin),
                (le, ":troop_no", 0),
                (assign, ":troop_no", "$g_talk_troop"),
            (try_end),
            (call_script, "script_companions_talk_info", ":troop_no"),
        ],
    ),
]