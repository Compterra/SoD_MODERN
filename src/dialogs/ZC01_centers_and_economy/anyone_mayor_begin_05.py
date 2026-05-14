DIALOGS = [
[anyone, "mayor_begin", [(check_quest_active, "qst_move_cattle_herd"),
                          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_failed, "qst_move_cattle_herd"),
                          ],
   "Word reached me before you did: the herd bound for {s9} is gone.\
 That is not just lost coin, {sir/madam}; it is empty butcher hooks, unpaid drovers, and another winter argument in the council room.\
 Tell me how I am supposed to answer for this.", "move_cattle_herd_failed",
   []],
]
