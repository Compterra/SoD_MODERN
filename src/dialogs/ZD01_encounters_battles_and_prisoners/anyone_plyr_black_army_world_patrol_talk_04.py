DIALOGS = [
[anyone|plyr, "black_army_world_patrol_talk", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 500),
  ], "Take 500 denars for a road-security contract.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 500),
    (call_script, "script_sod_black_army_apply_player_action", sod_black_army_action_security_contract, 500),
    (party_add_xp, "p_main_party", 150),
    (display_message, "@The Black Army records your security contract and marks nearby roads for patrol.", 0x444444),
    (assign, "$g_leave_encounter", 1),
  ]],
]
