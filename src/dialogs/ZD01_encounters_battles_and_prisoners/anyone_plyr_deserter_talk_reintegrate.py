DIALOGS = [
[anyone|plyr, "deserter_talk", [
    (gt, "$players_kingdom", 0),
    (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
    (ge, ":persuasion", 2),
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (le, ":enemy_size", 12),
    (neg|party_slot_eq, "$g_encountered_party", slot_party_sod_threat_sponsor_faction, "$players_kingdom"),
], "Come back under lawful colors. I will speak for you with my realm.", "deserter_reintegrate_offer", []],
]
