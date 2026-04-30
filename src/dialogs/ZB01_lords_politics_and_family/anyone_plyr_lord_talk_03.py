DIALOGS = [
[anyone|plyr, "lord_talk", [(call_script, "script_cf_prepare_collect_debt_offer", "$g_talk_troop"),
                            (neq, reg0, "qst_collect_debt")],
   "I've come to collect the debt you owe to {s1}.", "lord_ask_to_collect_debt_gm",
   [(assign, "$g_convince_quest", reg0)]],
]
