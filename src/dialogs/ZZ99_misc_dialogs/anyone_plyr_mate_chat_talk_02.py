DIALOGS = [
[anyone|plyr, "mate_chat_talk", [
  (neg|party_slot_eq, "$g_encountered_party", slot_party_type, spt_player_mercenaries),
  ], "I want to reorganize regiment.", "mate_chat_pre_talk",
    [
      (change_screen_exchange_members, 0),
    ]  ],
]
