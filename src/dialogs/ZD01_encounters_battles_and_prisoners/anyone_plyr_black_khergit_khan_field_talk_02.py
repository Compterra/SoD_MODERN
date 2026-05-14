DIALOGS = [
[anyone|plyr, "black_khergit_khan_field_talk", [
   (gt, "$players_kingdom", 0),
   (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
   (ge, ":renown", 300),
  ], "My enemies are richer prey. Turn the horde against them.", "close_window", [
    (call_script, "script_sod_black_khergits_apply_player_action", sod_black_khergit_action_persuade_enemy, 1),
    (display_message, "@Temujin weighs your reputation and angles the horde toward enemy lands.", 0x222222),
    (assign, "$g_leave_encounter", 1),
  ]],
]
