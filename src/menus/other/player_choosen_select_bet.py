MENUS = [
("player_choosen_select_bet", 0, 
  "Your opponent is ready.^^Current bet: {reg1?{reg1} denars:no bet}",
  "none",[
  (assign, reg1, "$g_jotnar_clan_competition_bet"),
  ],
  [
  ("fight", [], "Fight.", [
  (quest_get_slot, ":opp_troop", "qst_jotnar_clan_competition", slot_quest_target_troop),
  (modify_visitors_at_site, "scn_jotnar_clan_arena"),
  (reset_visitors),
  (try_begin),
	(eq, "$jc_wep_set", 1),
	(set_visitor, 11, ":opp_troop"),
	(set_jump_entry, 21),
  (else_try),
	(eq, "$jc_wep_set", 2),
	(set_visitor, 12, ":opp_troop"),
	(set_visitor, 22, "trp_player"),
  (else_try),
	(eq, "$jc_wep_set", 3),
	(set_visitor, 13, ":opp_troop"),
	(set_visitor, 23, "trp_player"),
  (else_try),
	(set_visitor, 14, ":opp_troop"),
	(set_visitor, 24, "trp_player"),
  (try_end),
  # (troop_remove_gold, "trp_player", "$g_jotnar_clan_competition_bet"),
  (set_jump_mission, "mt_jotnar_clan_arena"),
  (jump_to_scene, "scn_jotnar_clan_arena"),
  (change_screen_mission),
  ]),
  
  ("change_bet", [], "Change bet value.", [
  (assign, "$g_next_menu", "mnu_player_choosen_select_bet"),
  (jump_to_menu, "mnu_jc_change_bet"),]),
  
  ("back", [], "Back.",
  [(jump_to_menu, "mnu_jotnar_clan_competition"),
  ]),
  ]),
]
