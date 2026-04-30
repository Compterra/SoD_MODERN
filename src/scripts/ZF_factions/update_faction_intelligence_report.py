try:
    from src.compiler import *
except ImportError:
    from src.module_system import *

from src.constants.module_constants import *

SCRIPTS = [
    (
        "update_faction_intelligence_report",
        [
            (store_script_param, ":faction_no", 1),
            (store_script_param, ":focus_faction", 2),

            (assign, ":current_day", 0),
            (assign, ":cached_day", -1),

            (store_current_day, ":current_day"),
            (faction_get_slot, ":cached_day", ":faction_no", slot_faction_intelligence_report_day),

            (try_begin),
                (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
                (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
                (try_begin),
                    (eq, ":cached_day", ":current_day"),
                    (faction_get_slot, reg0, ":faction_no", slot_faction_intelligence_score),
                    (faction_get_slot, reg1, ":faction_no", slot_faction_intelligence_pressure),
                    (faction_get_slot, reg2, ":faction_no", slot_faction_intelligence_power_rank),
                    (faction_get_slot, reg3, ":faction_no", slot_faction_intelligence_growth),
                    (faction_get_slot, reg4, ":faction_no", slot_faction_intelligence_center_count),
                    (faction_get_slot, reg5, ":faction_no", slot_faction_intelligence_enemy_count),
                    (faction_get_slot, reg6, ":faction_no", slot_faction_intelligence_truce_count),
                    (faction_get_slot, reg7, ":faction_no", slot_faction_intelligence_marshal_present),
                    (faction_get_slot, reg8, ":faction_no", slot_faction_intelligence_vassal_count),
                (else_try),
                    (call_script, "script_estimate_faction_situation", ":faction_no", ":focus_faction"),

                    (faction_set_slot, ":faction_no", slot_faction_intelligence_report_day, ":current_day"),
                    (faction_set_slot, ":faction_no", slot_faction_intelligence_score, reg0),
                    (faction_set_slot, ":faction_no", slot_faction_intelligence_pressure, reg1),
                    (faction_set_slot, ":faction_no", slot_faction_intelligence_power_rank, reg2),
                    (faction_set_slot, ":faction_no", slot_faction_intelligence_growth, reg3),
                    (faction_set_slot, ":faction_no", slot_faction_intelligence_center_count, reg4),
                    (faction_set_slot, ":faction_no", slot_faction_intelligence_enemy_count, reg5),
                    (faction_set_slot, ":faction_no", slot_faction_intelligence_truce_count, reg6),
                    (faction_set_slot, ":faction_no", slot_faction_intelligence_marshal_present, reg7),
                    (faction_set_slot, ":faction_no", slot_faction_intelligence_vassal_count, reg8),
                (try_end),
            (else_try),
                (assign, reg0, 0),
                (assign, reg1, 0),
                (assign, reg2, 3),
                (assign, reg3, 4),
                (assign, reg4, 0),
                (assign, reg5, 0),
                (assign, reg6, 0),
                (assign, reg7, 0),
                (assign, reg8, 0),

                (faction_set_slot, ":faction_no", slot_faction_intelligence_report_day, ":current_day"),
                (faction_set_slot, ":faction_no", slot_faction_intelligence_score, 0),
                (faction_set_slot, ":faction_no", slot_faction_intelligence_pressure, 0),
                (faction_set_slot, ":faction_no", slot_faction_intelligence_power_rank, 3),
                (faction_set_slot, ":faction_no", slot_faction_intelligence_growth, 4),
                (faction_set_slot, ":faction_no", slot_faction_intelligence_center_count, 0),
                (faction_set_slot, ":faction_no", slot_faction_intelligence_enemy_count, 0),
                (faction_set_slot, ":faction_no", slot_faction_intelligence_truce_count, 0),
                (faction_set_slot, ":faction_no", slot_faction_intelligence_marshal_present, 0),
                (faction_set_slot, ":faction_no", slot_faction_intelligence_vassal_count, 0),
            (try_end),
        ],
    ),
]
