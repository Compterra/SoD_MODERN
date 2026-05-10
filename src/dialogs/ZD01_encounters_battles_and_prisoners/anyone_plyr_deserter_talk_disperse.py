DIALOGS = [
[anyone|plyr, "deserter_talk", [
    (party_get_num_companions, ":player_size", "p_main_party"),
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (le, ":enemy_size", 18),
    (store_mul, ":needed_size", ":enemy_size", 2),
    (ge, ":player_size", ":needed_size"),
], "Throw down your arms and scatter. If I see this band again, mercy ends.", "deserter_disperse_demand", []],
]
