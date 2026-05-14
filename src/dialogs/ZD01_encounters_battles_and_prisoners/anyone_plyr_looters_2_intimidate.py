DIALOGS = [
[anyone|plyr, "looters_2", [
    (party_get_num_companions, ":player_size", "p_main_party"),
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (store_mul, ":needed_size", ":enemy_size", 2),
    (ge, ":player_size", ":needed_size"),
], "Look at my banner, then count your boots. You still have time to use them.", "bandit_intimidate", []],
]
