DIALOGS = [
[anyone|plyr, "village_elder_talk", [(check_quest_active, "$g_cur_fugitive_quest"),
                                      (neg|check_quest_concluded, "$g_cur_fugitive_quest"),
                                      (quest_slot_eq, "$g_cur_fugitive_quest", slot_quest_target_center, "$current_town"),
                                      (quest_get_slot, ":quest_target_dna", "$g_cur_fugitive_quest", slot_quest_target_dna),
                                      (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
                                      (str_store_string_reg, s4, s50),
                                      ],
   "I am looking for a man by the name of {s4}. I was told he may be hiding here.", "village_elder_ask_fugitive", []],
]
