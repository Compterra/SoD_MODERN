DIALOGS = [
[anyone|plyr, "deserter_talk", [
    (party_get_num_companions, ":player_size", "p_main_party"),
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (le, ":enemy_size", 10),
    (store_mul, ":needed_size", ":enemy_size", 3),
    (ge, ":player_size", ":needed_size"),
    (party_get_free_prisoners_capacity, ":free_capacity", "p_main_party"),
    (gt, ":free_capacity", 0),
], "Kneel and be bound. A court can decide what your captain forgot.", "deserter_prisoner_demand", []],
]
