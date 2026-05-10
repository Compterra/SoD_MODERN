DIALOGS = [
[anyone|plyr, "mate_give_order", [], "Follow me", "mate_chat_pre_talk", [
    (call_script, "script_sod_external_party_set_order", "$g_encountered_party", sod_external_order_follow_player, "p_main_party"),
    (assign, "$g_encountered_party", reg0),
  ]],
]
