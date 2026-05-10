DIALOGS = [
[anyone, "bandit_shakedown_demand", [
    (party_get_num_companions, ":player_size", "p_main_party"),
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (store_mul, ":needed_size", ":enemy_size", 3),
    (this_or_next|ge, ":player_size", ":needed_size"),
    (store_random_in_range, ":nerve", 0, 100),
    (lt, ":nerve", 35),
], "Take it, then. Better poor than dead.", "close_window", [
    (store_random_in_range, ":loot_gold", 60, 181),
    (troop_add_gold, "trp_player", ":loot_gold"),
    (call_script, "script_sod_note_hostile_reputation", 6),
    (call_script, "script_sod_resolve_hostile_party_noncombat", "$g_encountered_party"),
    (display_message, "@The bandits surrender a rough purse of coin and disappear into the scrub."),
]],
]
