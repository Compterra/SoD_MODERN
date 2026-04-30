try:
    from src.compiler import *
except ImportError:
    from src.module_system import *

from src.constants.module_constants import *

SCRIPTS = [
    (
        "diplomacy_start_peace_between_kingdoms",
        [
            (store_script_param_1, ":faction_a"),
            (store_script_param_2, ":faction_b"),
            (store_script_param, ":initializing_war_peace_cond", 3),

            (try_begin),
                (neq, ":faction_a", ":faction_b"),

                (store_current_day, ":current_day"),
                (assign, ":truce_day", ":current_day"),
                (val_add, ":truce_day", 21),

                (assign, ":truce_slot_ab", slot_faction_truce_player_realm),
                (val_add, ":truce_slot_ab", ":faction_b"),
                (assign, ":truce_slot_ba", slot_faction_truce_player_realm),
                (val_add, ":truce_slot_ba", ":faction_a"),

                (try_begin),
                    (is_between, ":truce_slot_ab", slot_faction_truce_player_realm, faction_truce_slots_end),
                    (faction_get_slot, ":existing_truce_ab", ":faction_a", ":truce_slot_ab"),
                    (gt, ":existing_truce_ab", ":truce_day"),
                    (assign, ":truce_day", ":existing_truce_ab"),
                (try_end),
                (try_begin),
                    (is_between, ":truce_slot_ba", slot_faction_truce_player_realm, faction_truce_slots_end),
                    (faction_get_slot, ":existing_truce_ba", ":faction_b", ":truce_slot_ba"),
                    (gt, ":existing_truce_ba", ":truce_day"),
                    (assign, ":truce_day", ":existing_truce_ba"),
                (try_end),

                (try_begin),
                    (is_between, ":truce_slot_ab", slot_faction_truce_player_realm, faction_truce_slots_end),
                    (faction_set_slot, ":faction_a", ":truce_slot_ab", ":truce_day"),
                (try_end),
                (try_begin),
                    (is_between, ":truce_slot_ba", slot_faction_truce_player_realm, faction_truce_slots_end),
                    (faction_set_slot, ":faction_b", ":truce_slot_ba", ":truce_day"),
                (try_end),

                (store_relation, ":current_relation", ":faction_a", ":faction_b"),
                (val_max, ":current_relation", 0),
                (set_relation, ":faction_a", ":faction_b", ":current_relation"),

                (faction_set_slot, ":faction_a", slot_faction_last_refused_peace, 0),
                (faction_set_slot, ":faction_b", slot_faction_last_refused_peace, 0),

                (call_script, "script_event_kingdom_make_peace_with_kingdom", ":faction_a", ":faction_b"),

                (try_begin),
                    (eq, ":initializing_war_peace_cond", 0),
                    (this_or_next|eq, ":faction_a", fac_player_supporters_faction),
                    (eq, ":faction_b", fac_player_supporters_faction),
                    (str_store_faction_name, s1, ":faction_a"),
                    (str_store_faction_name, s2, ":faction_b"),
                    (display_message, "@Peace has been concluded between {s1} and {s2}.", 0x66CCFF),
                (try_end),
            (try_end),
        ],
    ),
]
