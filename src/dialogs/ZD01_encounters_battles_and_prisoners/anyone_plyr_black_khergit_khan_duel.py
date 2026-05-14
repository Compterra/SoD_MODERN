DIALOGS = [
[anyone|plyr, "black_khergit_khan_talk", [
    (troop_get_inventory_slot, ":player_horse", "trp_player", ek_horse),
    (gt, ":player_horse", 0),
  ], "If silver and words cannot move you, ride out and face me alone.", "close_window", [
    (assign, "$g_leave_encounter", 1),
    (jump_to_menu, "mnu_sod_black_khergit_khan_duel_prepare"),
    (finish_mission),
  ]],
]
