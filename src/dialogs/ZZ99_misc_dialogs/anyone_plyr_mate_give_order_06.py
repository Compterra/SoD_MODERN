DIALOGS = [
[anyone|plyr, "mate_give_order", [], "No new order. Keep the current detail steady.", "mate_chat_pre_talk", [
    (call_script, "script_sod_external_party_set_order", "$g_encountered_party", sod_external_order_noop, -1),
  ]],
]
