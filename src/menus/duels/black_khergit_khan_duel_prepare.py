MENUS = [
("sod_black_khergit_khan_duel_prepare", 0,
  "Temujin Black Sky rides out from the horde. His guards fall back, leaving only the two horses and the open field.",
  "none", [],
  [
    ("continue", [], "Begin the duel.", [
      (assign, "$g_sod_black_khergit_duel_active", 1),
      (assign, "$g_sod_convince_duel_won", 0),
      (assign, "$g_sod_dueled_troop", "trp_black_khergit_khan"),
      (assign, "$g_battle_result", 0),
      (assign, "$g_engaged_enemy", 0),
      (set_jump_entry, 56),
      (modify_visitors_at_site, "scn_random_scene"),
      (reset_visitors),
      (set_visitor, 56, "trp_player"),
      (set_visitor, 58, "trp_black_khergit_khan"),
      (set_jump_mission, "mt_sod_arena_duel_fight"),
      (jump_to_scene, "scn_random_scene"),
      (change_screen_mission),
    ]),
  ]),
]
