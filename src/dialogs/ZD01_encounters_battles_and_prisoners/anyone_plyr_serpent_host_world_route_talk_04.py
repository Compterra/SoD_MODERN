DIALOGS = [
[anyone|plyr, "serpent_host_world_route_talk", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 250),
  ], "Sell me road intelligence.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 250),
    (call_script, "script_sod_serpent_host_apply_player_action", sod_serpent_action_buy_intel, 8),
    (party_add_xp, "p_main_party", 150),
    (display_message, "@Serpent Host scouts mark fresh warnings and usable routes on your maps.", 0x66AA66),
    (assign, "$g_leave_encounter", 1),
  ]],
]
