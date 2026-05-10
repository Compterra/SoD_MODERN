DIALOGS = [
[anyone|plyr, "prisoner_chat", [
  (neg|troop_is_hero, "$g_talk_troop"),
  (neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
  (neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_mercenary_lord),
  ], "You there!", "prisoner_chat_commoner", []],
]
