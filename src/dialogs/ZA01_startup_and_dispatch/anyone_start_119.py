DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_tavern_talk),
                     (eq, "$g_talk_troop", "trp_farmer_from_bandit_village"),
                     (check_quest_active, "qst_eliminate_bandits_infesting_village"),
                     ],
   "Thank you for helping us {sir/madam}. Crush those bandits!", "close_window", []],
]
