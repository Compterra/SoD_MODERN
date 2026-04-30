MISSION_TEMPLATES = [
(
    "sod_arena_duel_fight_honor", mtf_arena_fight|mtf_commit_casualties, -1,
    "You enter a melee fight in the arena.",
    [
      (56, mtef_visitor_source|mtef_team_0, 0, aif_start_alarmed, 1, []),
      (58, mtef_visitor_source|mtef_team_2, 0, aif_start_alarmed, 1, []),
    ],
    [
      common_inventory_not_available,
	  common_battle_horse_health,
      (ti_tab_pressed, 0, 0, [(display_message, "@Cannot leave now.", red)], []),
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_arena),
         ]),

      (1, 4, ti_once, [(this_or_next|main_hero_fallen), (num_active_teams_le, 1)],
       [
           (try_begin),
             (main_hero_fallen),
             (call_script, "script_change_troop_renown", "trp_player", -10),
			(call_script, "script_change_player_honor", 2),
			(assign, "$g_sod_convince_duel_won", 0),
           (else_try),
             (call_script, "script_change_troop_renown", "trp_player", 5),
			(call_script, "script_change_player_honor", 5),
			(assign, "$g_sod_convince_duel_won", 1),
           (try_end),
		   (finish_mission),
		   (jump_to_menu, "mnu_sod_continue_return"),
           ]),
    ],
  ),
]
