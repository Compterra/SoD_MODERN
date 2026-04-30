DIALOGS = [
[anyone|plyr, "mayor_talk", [(store_partner_quest, ":partner_quest"),
                              (lt, ":partner_quest", 0),
                              (eq, "$merchant_quest_last_offerer", "$g_talk_troop"),
                              (ge, "$merchant_offered_quest", 0)
                              ],
   "About that job you offered me...", "merchant_quest_last_offered_job", []],
]
