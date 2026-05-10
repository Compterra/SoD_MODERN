DIALOGS = [
[anyone|plyr, "black_khergit_camp_talk", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 500),
  ], "Take 500 denars and keep your riders from my path.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 500),
    (call_script, "script_sod_black_khergits_apply_player_action", sod_black_khergit_action_tribute, 500),
    (store_current_hours, ":protected_until"),
    (val_add, ":protected_until", 96),
    (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, ":protected_until"),
    (party_ignore_player, "$g_encountered_party", 96),
    (display_message, "@The Black Khergits accept tribute and grant you a short-lived road peace.", 0x222222),
    (assign, "$g_leave_encounter", 1),
  ]],
]
