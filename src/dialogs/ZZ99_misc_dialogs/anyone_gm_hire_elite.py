DIALOGS = [
[anyone,"gm_hire_elite", [(eq, "$g_rep", "$g_talk_troop"),
   (call_script, "script_merc_get_elite_relation_requirement", "$g_talk_troop_faction"),
   (ge, "$g_talk_troop_faction_relation", reg0),], "I have some guards at this location I can hire out to you immediately", "gm_pretalk",[(set_mercenary_source_party,"$gm_party_elite"),[change_screen_buy_mercenaries]]],
]
