DIALOGS = [
[anyone|plyr, "prisoner_chat", [
  (neg|troop_is_hero, "$g_talk_troop"),
  (troop_slot_eq, "$g_talk_troop", slot_prisoner_agreed, 1),
  (neg|troops_can_join, 1),
  ], "I am sorry, I still have no room for you. You'll have to wait a while longer.", "close_window", []],
]
