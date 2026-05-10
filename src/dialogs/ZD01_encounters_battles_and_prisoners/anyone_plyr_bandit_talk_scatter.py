DIALOGS = [
[anyone|plyr, "bandit_talk", [
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (le, ":enemy_size", 10),
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (ge, ":renown", 150),
], "Run before I bother learning your names.", "bandit_scatter_demand", []],
]
