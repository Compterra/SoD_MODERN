DIALOGS = [
[anyone, "lord_leave", [
      (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
      (lt, "$g_talk_troop_faction_relation", 0),
      (store_partner_quest, ":enemy_lord_quest"),
      (lt, ":enemy_lord_quest", 0),
      (troop_slot_eq, "$g_talk_troop", slot_troop_does_not_give_quest, 0),
      (call_script, "script_get_random_quest", "$g_talk_troop"),
      (assign, "$random_quest_no", reg0),
      (ge, "$random_quest_no", 0),
    ],
   "Before you go, {playername}, I have something to ask of you... We may be enemies in this war,\
 but I pray that you believe, as I do, that we can still be civil towards each other.\
 Thus I hoped that you would be kind enough to assist me in something important to me.", "lord_leave_give_quest", []],
]
