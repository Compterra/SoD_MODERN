DIALOGS = [
[anyone|plyr, "deserter_talk", [
    (ge, "$player_honor", 15),
    (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
    (ge, ":persuasion", 2),
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (le, ":enemy_size", 8),
], "Not soldiers, then. Refugees. Leave your arms and I will see you protected.", "deserter_refugee_offer", []],
]
