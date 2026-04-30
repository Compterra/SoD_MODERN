DIALOGS = [
[anyone|plyr, "gm_hire3", [
   (faction_get_slot, ":mercenaries", "fac_player_faction", slot_faction_merc_pact),
   (this_or_next|eq, ":mercenaries", "$g_talk_troop_faction"),
   (ge, "$g_talk_troop_faction_relation", 25),
   ],"100", "gm_hire4", [
   (assign, "$temp1", 100),]],
]
