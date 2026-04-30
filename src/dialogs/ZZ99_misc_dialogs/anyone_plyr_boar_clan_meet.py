DIALOGS = [
[anyone|plyr, "boar_clan_meet", [], "I'm up for some boar killing! Squeal, piggies!", "boar_clan_attack",
   [(party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, 0),
    (call_script, "script_change_player_relation_with_faction", "fac_sod_merc_guild7", -15),
    ]],
]
