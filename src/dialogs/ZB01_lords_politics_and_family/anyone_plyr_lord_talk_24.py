DIALOGS = [
[anyone|plyr, "lord_talk", [
  (eq, 0, 1),#DISABLE
  (eq, "$g_talk_troop_faction", "fac_player_supporters_faction"),
                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             ],
   "I want to give some gold to you.", "lord_give_money", []],
]
