DIALOGS = [
[anyone|plyr, "mayor_talk", [(store_partner_quest, ":partner_quest"),
                              (lt, ":partner_quest", 0),
                              (neq, "$merchant_quest_last_offerer", "$g_talk_troop")],
   "Do you happen to have a job for me?", "merchant_quest_requested", [
     (assign, "$merchant_quest_last_offerer", "$g_talk_troop"),
     (call_script, "script_get_random_quest", "$g_talk_troop"),
     (assign, "$random_merchant_quest_no", reg0),
     (assign, "$merchant_offered_quest", "$random_merchant_quest_no"),
     ]],
]
