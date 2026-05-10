DIALOGS = [
[anyone|plyr, "serpent_host_world_route_talk", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 300),
  ], "I want safe passage through your watched roads.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 300),
    (call_script, "script_sod_serpent_host_apply_player_action", sod_serpent_action_safe_passage, 10),
    (store_current_hours, ":protected_until"),
    (val_add, ":protected_until", 96),
    (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, ":protected_until"),
    (party_ignore_player, "$g_encountered_party", 96),
    (display_message, "@The Serpent Host grants you temporary safe passage on watched roads.", 0x66AA66),
    (assign, "$g_leave_encounter", 1),
  ]],
]
