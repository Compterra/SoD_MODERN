DIALOGS = [
[anyone|plyr, "gm_talk", [(store_partner_quest, "$g_lords_quest"),
                                         (this_or_next|eq, "$g_lords_quest", "qst_elephant_guard_hunt_down_fugitive"),
                                         (this_or_next|eq, "$g_lords_quest", "qst_bc_hunt_down_fugitive"),
										 (eq, "$g_lords_quest", "qst_conquistadors_hunt_down_fugitive"),
                                         (check_quest_succeeded, "$g_lords_quest"),
                                         (quest_get_slot, ":quest_target_center", "$g_lords_quest", slot_quest_target_center),
                                         (str_store_party_name, s3, ":quest_target_center"),
     ],
   "I found the thief hiding at {s3} and gave him his punishment.", "gm_hunt_down_fugitive_success",
   []],
]
