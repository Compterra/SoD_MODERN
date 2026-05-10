DIALOGS = [
[anyone|plyr, "black_khergit_khan_talk", [
    (troop_get_inventory_slot, ":player_horse", "trp_player", ek_horse),
    (gt, ":player_horse", 0),
  ], "If silver and words cannot move you, ride out and face me alone.", "close_window", [
    (assign, "$g_sod_black_khergit_duel_active", 1),
    (assign, "$g_sod_convince_duel_won", 0),
    (assign, "$g_sod_dueled_troop", "trp_black_khergit_khan"),
    (modify_visitors_at_site, "scn_random_scene"),
    (reset_visitors),
    (set_visitor, 56, "trp_player"),
    (set_visitor, 58, "trp_black_khergit_khan"),
    (set_jump_mission, "mt_sod_arena_duel_fight"),
    (jump_to_scene, "scn_random_scene"),
    (change_screen_mission),
  ]],
]
