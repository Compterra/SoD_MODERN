DIALOGS = [
[anyone|plyr, "mate_chat_talk", [
  (neg|party_slot_eq, "$g_encountered_party", slot_party_type, spt_player_mercenaries),
  ], "I want to reorganize regiment.", "mate_chat_pre_talk",
    [
      (call_script, "script_game_get_party_companion_limit", 3),
      (display_message, "@allowed party size {reg0}", green),
      (change_screen_exchange_members, 0),
      (store_encountered_party, ":cur_party"),
      (call_script, "script_cf_fix_party_size", ":cur_party", 1),
    ]  ],
]
