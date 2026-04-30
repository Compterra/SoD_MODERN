DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_lend_surgeon"),
                         (quest_slot_eq, "qst_lend_surgeon", slot_quest_giver_troop, "$g_talk_troop")],
   "Your surgeon managed to convince my friend and made the operation.  The matter is in God's hands now, , and all we can do is pray for his recovery.\
 Anyway, I thank you for lending your surgeon to me {sir/madam}. You have a noble spirit. I will not forget it.", "lord_generic_mission_completed",
   [
     (call_script, "script_finish_quest", "qst_lend_surgeon", 100),
     (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
     ]],
]
