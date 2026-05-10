DIALOGS = [
[anyone|plyr, "conquistador_world_logistics_talk", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 300),
  ], "I can carry a delivery bond for your quartermasters.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 300),
    (call_script, "script_sod_conquistador_apply_player_action", sod_conquistador_action_delivery_contract, 300),
    (party_add_xp, "p_main_party", 200),
    (display_message, "@The Conquistadors mark you as a useful supply contractor.", 0xCCAA55),
    (assign, "$g_leave_encounter", 1),
  ]],
]
