try:
    from src.compiler import *
except:
    from src.module_system import *

from src.constants.module_constants import *


SCRIPTS = [
    (
        "update_center_population_supply",
        [
            (store_script_param, ":center_no", 1),
            (try_begin),
                (gt, ":center_no", 0),
                (party_get_slot, ":population", ":center_no", slot_center_sod_local_population),
                (party_get_slot, ":health", ":center_no", slot_center_sod_local_health),
                (party_get_slot, ":prosperity", ":center_no", slot_center_sod_local_prosperity),
                (party_get_slot, ":wealth", ":center_no", slot_town_wealth),
                (assign, ":population_change", 0),
                (try_begin),
                    (gt, ":health", 0),
                    (store_div, ":health_bonus", ":health", 50),
                    (val_add, ":population_change", ":health_bonus"),
                (try_end),
                (try_begin),
                    (gt, ":prosperity", 0),
                    (store_div, ":prosperity_bonus", ":prosperity", 200),
                    (val_add, ":population_change", ":prosperity_bonus"),
                (try_end),
                (try_begin),
                    (gt, ":wealth", 0),
                    (store_div, ":wealth_bonus", ":wealth", 5000),
                    (val_add, ":population_change", ":wealth_bonus"),
                (else_try),
                    (lt, ":wealth", 0),
                    (val_sub, ":population_change", 1),
                (try_end),
                (val_add, ":population", ":population_change"),
                (val_max, ":population", 0),
                (party_set_slot, ":center_no", slot_center_sod_local_population, ":population"),
            (try_end),
        ],
    ),
    (
        "get_center_recruitable_population",
        [
            (store_script_param, ":center_no", 1),
            (store_script_param, ":requested_amount", 2),
            (assign, reg0, 0),
            (try_begin),
                (gt, ":center_no", 0),
                (party_get_slot, ":population", ":center_no", slot_center_sod_local_population),
                (store_sub, ":available", ":population", village_pop_min),
                (val_max, ":available", 0),
                (try_begin),
                    (gt, ":requested_amount", 0),
                    (val_min, ":available", ":requested_amount"),
                (try_end),
                (assign, reg0, ":available"),
            (try_end),
        ],
    ),
    (
        "spend_center_population_for_recruitment",
        [
            (store_script_param, ":center_no", 1),
            (store_script_param, ":recruit_count", 2),
            (try_begin),
                (gt, ":center_no", 0),
                (gt, ":recruit_count", 0),
                (party_get_slot, ":population", ":center_no", slot_center_sod_local_population),
                (val_sub, ":population", ":recruit_count"),
                (val_max, ":population", village_pop_min),
                (party_set_slot, ":center_no", slot_center_sod_local_population, ":population"),
            (try_end),
        ],
    ),
]
