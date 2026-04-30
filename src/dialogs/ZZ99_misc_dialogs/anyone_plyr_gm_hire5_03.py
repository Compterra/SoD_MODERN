DIALOGS = [
[anyone|plyr, "gm_hire5", [
   (faction_get_slot, ":mercenaries", "fac_player_faction", slot_faction_merc_pact),
   (this_or_next|eq, ":mercenaries", "$g_talk_troop_faction"),
   (ge, "$g_talk_troop_faction_relation", 35),
   ],"Experienced.", "gm_hire6", [
   (assign, "$temp2", 3),]],
]
