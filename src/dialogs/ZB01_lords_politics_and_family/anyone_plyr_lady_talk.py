DIALOGS = [
[anyone|plyr, "lady_talk",
   [
     (store_partner_quest, ":ladys_quest"),
     (lt, ":ladys_quest", 0)
     ],
   "Is there anything I can do to win your favour?", "lady_ask_for_quest", [(call_script, "script_get_random_quest", "$g_talk_troop"),
                                                                 (assign, "$random_quest_no", reg0)]],
]
