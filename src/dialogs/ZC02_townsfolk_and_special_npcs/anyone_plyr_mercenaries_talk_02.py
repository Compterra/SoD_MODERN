DIALOGS = [
[anyone|plyr, "mercenaries_talk", [
  (store_troop_gold, ":gold", "trp_player"),
  (ge, ":gold", reg1),
  (gt, "$g_encountered_party", 0),
  (neq, "$g_encountered_party", "p_main_party"),
  (party_is_active, "$g_encountered_party"),
  (party_can_join, "$g_encountered_party"),
  ], "All right, you are hired.", "close_window", [
  (call_script, "script_party_add_party", "p_main_party", "$g_encountered_party"),
  (remove_party, "$g_encountered_party"),
  (call_script, "script_sod_player_charge_gold", reg1),
  (assign, "$g_leave_encounter", 1),
  ]],
]
