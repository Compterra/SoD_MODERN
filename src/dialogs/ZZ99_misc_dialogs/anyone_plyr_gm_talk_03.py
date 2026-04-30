DIALOGS = [
[anyone|plyr, "gm_talk", [(store_partner_quest, ":lords_quest"),
                                         (this_or_next|eq, ":lords_quest", "qst_elephant_guard_hunt_down_fugitive"),
                                         (this_or_next|eq, ":lords_quest", "qst_bc_hunt_down_fugitive"),
										 (eq, ":lords_quest", "qst_conquistadors_hunt_down_fugitive"),
                                         (check_quest_failed, ":lords_quest"),
                                         ],
   "I'm afraid the thief got away.", "gm_hunt_down_fugitive_fail",
   []],
]
