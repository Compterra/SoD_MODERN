DIALOGS = [
[anyone|plyr, "event_triggered", [
    (store_conversation_troop, "$g_talk_troop"),
    (store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),
    (store_relation, "$g_talk_troop_faction_relation", "$g_talk_troop_faction", "fac_player_faction"),
    (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
    (assign, "$g_talk_troop_relation", reg0),
    (call_script, "script_setup_talk_info"),
    (eq, 1, 0)
  ], "", "close_window", []],
]
