DIALOGS = [
[anyone|plyr, "mate_give_order", [], "Patrol this area", "mate_chat_pre_talk", [
    (call_script, "script_sod_external_party_set_order", "$g_encountered_party", sod_external_order_patrol_here, -1),
    (assign, "$g_encountered_party", reg0),
  ]],
]
