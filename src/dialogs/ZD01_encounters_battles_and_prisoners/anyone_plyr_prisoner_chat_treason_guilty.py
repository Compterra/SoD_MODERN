DIALOGS = [
[anyone|plyr, "prisoner_chat_treason_guilty", [], "For your many crimes against {s1}, I hereby sentence you to death, to be carried out immediately.  Have you any final words to say?", "prisoner_chat_treason_final_words",
    [
      (store_random_in_range, reg0, 0, 100),
      (val_mod, reg0, 5),
      (troop_set_slot, "$g_talk_troop", slot_prisoner_agreed, reg0),
    ]
  ],
]
