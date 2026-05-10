DIALOGS = [
[anyone|plyr, "black_army_world_patrol_talk", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 350),
  ], "I need your patrol to screen my march.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 350),
    (call_script, "script_sod_black_army_apply_player_action", sod_black_army_action_hire_patrol, 350),
    (store_current_hours, ":protected_until"),
    (val_add, ":protected_until", 72),
    (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, ":protected_until"),
    (party_ignore_player, "$g_encountered_party", 72),
    (display_message, "@The Black Army patrol grants you temporary road cover.", 0x444444),
    (assign, "$g_leave_encounter", 1),
  ]],
]
