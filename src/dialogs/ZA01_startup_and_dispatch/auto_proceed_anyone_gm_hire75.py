DIALOGS = [
[auto_proceed|anyone, "gm_hire75", [
   (this_or_next|eq, "$g_talk_troop_faction", "fac_sod_merc_guild3"),
   (this_or_next|eq, "$g_talk_troop_faction", "fac_sod_merc_guild6"),
   (eq, "$g_talk_troop_faction", "fac_sod_merc_guild7"),
   ], "Continue", "gm_hire8", []],
]
