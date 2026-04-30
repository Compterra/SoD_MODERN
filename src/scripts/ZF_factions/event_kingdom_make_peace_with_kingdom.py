try:
    from src.compiler import *
except ImportError:
    from src.module_system import *

from src.constants.module_constants import *

SCRIPTS = [
    (
        "event_kingdom_make_peace_with_kingdom",
        [
            (store_script_param_1, ":faction_a"),
            (store_script_param_2, ":faction_b"),

            (try_begin),
                (neq, ":faction_a", ":faction_b"),
                (call_script, "script_update_faction_notes", ":faction_a"),
                (call_script, "script_update_faction_notes", ":faction_b"),
                (call_script, "script_update_faction_traveler_notes", ":faction_a"),
                (call_script, "script_update_faction_traveler_notes", ":faction_b"),
            (try_end),
        ],
    ),
]
