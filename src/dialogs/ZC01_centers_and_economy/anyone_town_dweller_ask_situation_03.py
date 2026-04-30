DIALOGS = [
[anyone, "town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         (assign, ":walker_type", reg0),
                                         (eq, ":walker_type", walkert_needs_money_helped)
                                         ],
   "Thank you for your kindness {sir/madam}. With your help our lives will be better. I will pray for you everyday.", "close_window", []],
]
