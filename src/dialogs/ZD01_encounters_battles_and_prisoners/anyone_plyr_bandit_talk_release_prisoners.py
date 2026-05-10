DIALOGS = [
[anyone|plyr, "bandit_talk", [
    (party_get_num_prisoners, ":prisoners", "$g_encountered_party"),
    (gt, ":prisoners", 0),
    (party_get_num_companions, ":player_size", "p_main_party"),
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (ge, ":player_size", ":enemy_size"),
], "Release your prisoners and I may let you leave with your skins.", "bandit_release_prisoners_demand", []],
]
