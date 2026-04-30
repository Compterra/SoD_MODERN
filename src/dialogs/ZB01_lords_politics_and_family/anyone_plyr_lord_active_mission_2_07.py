DIALOGS = [
[anyone|plyr, "lord_active_mission_2", [(store_partner_quest, ":lords_quest"),
                                         (eq, ":lords_quest", "qst_hunt_down_fugitive"),
                                         (check_quest_succeeded, "qst_hunt_down_fugitive"),
                                         (quest_get_slot, ":quest_target_center", "qst_hunt_down_fugitive", slot_quest_target_center),
                                         (str_store_party_name, s3, ":quest_target_center"),
                                         (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
                                         (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
                                         (str_store_string, s4, s50), ],
   "I found {s4} hiding at {s3} and gave him his punishment.", "lord_hunt_down_fugitive_success",
   []],
]
