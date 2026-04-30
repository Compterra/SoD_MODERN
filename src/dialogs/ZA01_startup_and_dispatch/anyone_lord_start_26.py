DIALOGS = [
[anyone, "lord_start", [(check_quest_active, "qst_report_to_army"),
                        (quest_slot_eq, "qst_report_to_army", slot_quest_target_troop, "$g_talk_troop"),
                        ],
   "Ah, you have arrived at last, {playername}. We've been expecting you. I hope you have brought with you troops of sufficient number and experience.", "lord_report_to_army_asked",
   []],
]
