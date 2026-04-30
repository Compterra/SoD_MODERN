DIALOGS = [
[anyone|plyr, "village_elder_talk", [(check_quest_active, "qst_hunt_down_fugitive"),
                                      (neg|check_quest_concluded, "qst_hunt_down_fugitive"),
                                      (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
                                      (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
                                      (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
                                      (str_store_string, s4, s50),
                                      ],
   "I am looking for a man by the name of {s4}. I was told he may be hiding here.", "village_elder_ask_fugitive", []],
]
