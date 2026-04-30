DIALOGS = [
[anyone, "boar_clan_attack2", [
      ], "Wha- how you dare! You are just like the tyrants who scattered the Clan in the first place! We'd sooner die than join you, villain! Wake up lads, it's time for fightin'!", "close_window", [
	  (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, 0),
      (call_script, "script_change_player_relation_with_faction", "fac_sod_merc_guild7", -5),
	  ]],
]
