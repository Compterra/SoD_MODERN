DIALOGS = [
[anyone, "mayor_begin", [(check_quest_active, "qst_deal_with_looters"),
                          (quest_slot_eq, "qst_deal_with_looters", slot_quest_giver_troop, "$g_talk_troop"),
                         ],
   "Ah, {playername}. The watch still counts empty stalls after every raid. Tell me you have news of those looters.", "mayor_looters_quest_response",
   [
    ]],
]
