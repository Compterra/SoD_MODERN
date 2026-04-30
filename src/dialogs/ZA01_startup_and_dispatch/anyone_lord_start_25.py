DIALOGS = [
[anyone, "lord_start",
   [
     (check_quest_active, "qst_follow_army"),
     (faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"),
     (eq, "$g_random_army_quest", "qst_deliver_cattle_to_army"),
     (quest_get_slot, ":quest_target_amount", "$g_random_army_quest", slot_quest_target_amount),
     (assign, reg3, ":quest_target_amount"),
     ],
   "The army's supplies are dwindling too quickly, {playername}. I need you to bring me {reg3} heads of cattle so I can keep the troops fed. I care very little about where you get them, just bring them to me as soon as you can.", "lord_mission_told_deliver_cattle_to_army",
   [
   ]
   ],
]
