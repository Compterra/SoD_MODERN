try:
    from src.compiler import *
except ImportError:
    from src.module_system import *

from src.constants.module_constants import *

SCRIPTS = [
    (
        "make_kingdom_hostile_to_player",
        [
            (store_script_param_1, ":faction_no"),

            (try_begin),
                (neq, ":faction_no", fac_player_supporters_faction),
                (call_script, "script_diplomacy_start_war_between_kingdoms", ":faction_no", fac_player_supporters_faction, 0),
            (try_end),
        ],
    ),
]
