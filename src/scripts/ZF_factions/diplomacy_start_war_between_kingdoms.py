try:
    from src.compiler import *
except ImportError:
    from src.module_system import *

from src.constants.module_constants import *

SCRIPTS = [
    (
        "diplomacy_start_war_between_kingdoms",
        [
            (store_script_param_1, ":faction_a"),
            (store_script_param_2, ":faction_b"),
            (store_script_param, ":initializing_war_peace_cond", 3),

            (try_begin),
                (neq, ":faction_a", ":faction_b"),

                (store_current_day, ":current_day"),

                (assign, ":truce_slot_ab", slot_faction_truce_player_realm),
                (val_add, ":truce_slot_ab", ":faction_b"),
                (assign, ":truce_slot_ba", slot_faction_truce_player_realm),
                (val_add, ":truce_slot_ba", ":faction_a"),

                (try_begin),
                    (is_between, ":truce_slot_ab", slot_faction_truce_player_realm, faction_truce_slots_end),
                    (faction_set_slot, ":faction_a", ":truce_slot_ab", 0),
                (try_end),
                (try_begin),
                    (is_between, ":truce_slot_ba", slot_faction_truce_player_realm, faction_truce_slots_end),
                    (faction_set_slot, ":faction_b", ":truce_slot_ba", 0),
                (try_end),

                (store_relation, ":current_relation", ":faction_a", ":faction_b"),
                (val_min, ":current_relation", -40),
                (set_relation, ":faction_a", ":faction_b", ":current_relation"),

                (try_begin),
                    (eq, ":initializing_war_peace_cond", 0),
                    (faction_set_slot, ":faction_a", slot_faction_last_big_offensive, ":current_day"),
                (try_end),

                (faction_set_slot, ":faction_a", slot_faction_last_started_war, ":faction_b"),
                (faction_set_slot, ":faction_a", slot_faction_last_started_war_date, ":current_day"),
                (faction_set_slot, ":faction_b", slot_faction_last_started_war, ":faction_a"),
                (faction_set_slot, ":faction_b", slot_faction_last_started_war_date, ":current_day"),

                (call_script, "script_update_faction_notes", ":faction_a"),
                (call_script, "script_update_faction_notes", ":faction_b"),
                (call_script, "script_update_faction_traveler_notes", ":faction_a"),
                (call_script, "script_update_faction_traveler_notes", ":faction_b"),

                (try_begin),
                    (eq, ":initializing_war_peace_cond", 0),
                    (this_or_next|eq, ":faction_a", fac_player_supporters_faction),
                    (eq, ":faction_b", fac_player_supporters_faction),
                    (str_store_faction_name, s1, ":faction_a"),
                    (str_store_faction_name, s2, ":faction_b"),
                    (display_message, "@War has broken out between {s1} and {s2}.", 0xFF4444),
                (try_end),
            (try_end),
        ],
    ),
]
