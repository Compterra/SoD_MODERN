DIALOGS = [
[anyone|plyr, "mate_chat_talk", [
  (neg|party_slot_eq, "$g_encountered_party", slot_party_type, spt_player_mercenaries),
  ], "I want to you to join me again.", "mate_chat_rejoin", []],
]
