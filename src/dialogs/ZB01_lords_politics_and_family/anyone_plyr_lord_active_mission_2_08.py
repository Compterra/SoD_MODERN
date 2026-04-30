DIALOGS = [
[anyone|plyr, "lord_active_mission_2", [(store_partner_quest, ":lords_quest"),
                                         (eq, ":lords_quest", "qst_hunt_down_fugitive"),
                                         (check_quest_failed, "qst_hunt_down_fugitive"),
                                         ],
   "I'm afraid he got away.", "lord_hunt_down_fugitive_fail",
   []],
]
