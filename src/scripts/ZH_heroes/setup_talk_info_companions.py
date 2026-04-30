from header_operations import *
from module_constants import *

SCRIPTS = [
    (
        "setup_talk_info_companions",
        [
            (store_script_param, ":troop_no", 1),
            (call_script, "script_companions_talk_info", ":troop_no"),
            (assign, ":troop_morale", reg0),
            (talk_info_set_relation_bar, ":troop_morale"),
            (talk_info_set_line, 0, s61),
            (talk_info_set_line, 1, s62),
            (talk_info_set_line, 2, s60),
            (talk_info_set_line, 3, s63),
        ],
    ),
]