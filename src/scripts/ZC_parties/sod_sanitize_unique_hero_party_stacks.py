try:
    from src.compiler import *
except ImportError:
    from src.module_system import *

from src.constants.module_constants import *

SCRIPTS = [
    (
        "sod_sanitize_unique_hero_party_stacks",
        [
            (assign, reg0, 0),

            (try_for_parties, ":party_no"),
                (neg|is_between, ":party_no", "p_temp_party", "p_town_merc_1"),
                (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
                (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
                    (party_stack_get_troop_id, ":stack_troop", ":party_no", ":stack_no"),
                    (troop_is_hero, ":stack_troop"),
                    (assign, ":remove_stack", 0),

                    (try_begin),
                        (eq, ":stack_troop", "trp_player"),
                        (neq, ":party_no", "p_main_party"),
                        (assign, ":remove_stack", 1),
                    (else_try),
                        (is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
                        (try_begin),
                            (eq, ":stack_no", 0),
                            (troop_slot_eq, ":stack_troop", slot_troop_leaded_party, ":party_no"),
                            (assign, ":remove_stack", 0),
                        (else_try),
                            (assign, ":remove_stack", 1),
                        (try_end),
                    (try_end),

                    (try_begin),
                        (eq, ":remove_stack", 1),
                        (party_stack_get_size, ":stack_size", ":party_no", ":stack_no"),
                        (party_remove_members, ":party_no", ":stack_troop", ":stack_size"),
                        (val_add, reg0, 1),
                        (try_begin),
                            (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_ai_mercenaries),
                            (party_slot_eq, ":party_no", slot_party_type, spt_mercenary_lord_party),
                            (party_get_num_companions, ":party_size_after", ":party_no"),
                            (le, ":party_size_after", 0),
                            (neq, ":party_no", "p_main_party"),
                            (remove_party, ":party_no"),
                        (try_end),
                    (try_end),
                (try_end),
            (try_end),
        ],
    ),
]
