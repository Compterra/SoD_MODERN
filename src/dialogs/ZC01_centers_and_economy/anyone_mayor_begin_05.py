DIALOGS = [
[anyone, "mayor_begin", [(check_quest_active, "qst_move_cattle_herd"),
                          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_failed, "qst_move_cattle_herd"),
                          ],
   "I heard that you have lost the cattle herd on your way to {s9}.\
 I had a very difficult time explaining your failure to the owner of that herd, {sir/madam}.\
 Do you have anything to say?", "move_cattle_herd_failed",
   []],
]
