DIALOGS = [
[anyone|plyr, "black_khergit_raider_talk", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 200),
  ], "Take 200 denars and ride elsewhere.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 200),
    (call_script, "script_sod_black_khergits_apply_player_action", sod_black_khergit_action_tribute, 200),
    (store_current_hours, ":protected_until"),
    (val_add, ":protected_until", 48),
    (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, ":protected_until"),
    (party_ignore_player, "$g_encountered_party", 48),
    (assign, "$g_leave_encounter", 1),
  ]],
]
