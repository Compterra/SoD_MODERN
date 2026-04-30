DIALOGS = [
[anyone, "town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         (assign, ":walker_type", reg0),
                                         (eq, ":walker_type", walkert_needs_money)],
   "My life is miserable, {sir/madam}. I haven't been able to find a job for months, and my poor children go to bed hungry each night.\
 My neighbours are too poor themselves to help me.", "town_dweller_poor", []],
]
