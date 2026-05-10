DIALOGS = [
[anyone|plyr, "bandit_talk", [
    (party_get_num_companions, ":player_size", "p_main_party"),
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (store_mul, ":needed_size", ":enemy_size", 2),
    (ge, ":player_size", ":needed_size"),
], "You wanted tribute. Empty your purses, and I may let you crawl away.", "bandit_shakedown_demand", []],
]
