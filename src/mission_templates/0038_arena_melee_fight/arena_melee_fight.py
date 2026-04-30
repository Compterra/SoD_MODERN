MISSION_TEMPLATES = [
(
    "arena_melee_fight", mtf_arena_fight, -1,
    "You enter a melee fight in the arena.",
    [
      (0, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_bow, itm_practice_arrows, itm_practice_horse, itm_arena_tunic_red, itm_red_tourney_helmet]),
      (1, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_arena_tunic_red]),
      (2, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_practice_horse, itm_arena_tunic_red, itm_red_tourney_helmet]),
      (3, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_lance, itm_practice_shield, itm_practice_horse, itm_arena_tunic_red, itm_red_tourney_helmet]),
      (4, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_bow, itm_practice_arrows, itm_arena_tunic_red]),
      (5, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield, itm_arena_tunic_red]),
      (6, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_practice_horse, itm_arena_tunic_red]),
      (7, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_lance, itm_practice_shield, itm_practice_horse, itm_arena_tunic_red, itm_red_tourney_helmet]),

      (8, mtef_visitor_source|mtef_team_1, af_override_all, aif_start_alarmed, 1, [itm_practice_bow, itm_practice_arrows, itm_arena_tunic_blue]),
      (9, mtef_visitor_source|mtef_team_1, af_override_all, aif_start_alarmed, 1, [itm_practice_lance, itm_practice_shield, itm_practice_horse, itm_arena_tunic_blue, itm_blue_tourney_helmet]),
      (10, mtef_visitor_source|mtef_team_1, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_arena_tunic_blue]),
      (11, mtef_visitor_source|mtef_team_1, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield, itm_arena_tunic_blue, itm_blue_tourney_helmet]),
      (12, mtef_visitor_source|mtef_team_1, af_override_all, aif_start_alarmed, 1, [itm_practice_bow, itm_practice_arrows, itm_practice_horse, itm_arena_tunic_blue]),
      (13, mtef_visitor_source|mtef_team_1, af_override_all, aif_start_alarmed, 1, [itm_practice_lance, itm_practice_shield, itm_practice_horse, itm_arena_tunic_blue, itm_blue_tourney_helmet]),
      (14, mtef_visitor_source|mtef_team_1, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_arena_tunic_blue]),
      (15, mtef_visitor_source|mtef_team_1, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield, itm_arena_tunic_blue]),

      (16, mtef_visitor_source|mtef_team_2, af_override_all, aif_start_alarmed, 1, [itm_practice_bow, itm_practice_arrows, itm_practice_horse, itm_arena_tunic_green, itm_green_tourney_helmet]),
      (17, mtef_visitor_source|mtef_team_2, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_arena_tunic_green, itm_green_tourney_helmet]),
      (18, mtef_visitor_source|mtef_team_2, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_practice_horse, itm_arena_tunic_green, itm_green_tourney_helmet]),
      (19, mtef_visitor_source|mtef_team_2, af_override_all, aif_start_alarmed, 1, [itm_practice_lance, itm_practice_shield, itm_practice_horse, itm_arena_tunic_green, itm_green_tourney_helmet]),
      (20, mtef_visitor_source|mtef_team_2, af_override_all, aif_start_alarmed, 1, [itm_practice_bow, itm_practice_arrows, itm_arena_tunic_green, itm_green_tourney_helmet]),
      (21, mtef_visitor_source|mtef_team_2, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield, itm_arena_tunic_green]),
      (22, mtef_visitor_source|mtef_team_2, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_practice_horse, itm_arena_tunic_green]),
      (23, mtef_visitor_source|mtef_team_2, af_override_all, aif_start_alarmed, 1, [itm_practice_lance, itm_practice_shield, itm_practice_horse, itm_arena_tunic_green, itm_green_tourney_helmet]),

      (24, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_practice_bow, itm_practice_arrows, itm_practice_horse, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (25, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (26, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_practice_horse, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (27, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_practice_lance, itm_practice_shield, itm_practice_horse, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (28, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_practice_bow, itm_practice_arrows, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (29, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield, itm_arena_tunic_yellow]),
      (30, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_practice_horse, itm_arena_tunic_yellow]),
      (31, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_practice_lance, itm_practice_shield, itm_practice_horse, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
#32
      (32, mtef_visitor_source|mtef_team_1, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword]),
      (33, mtef_visitor_source|mtef_team_2, af_override_all, aif_start_alarmed, 1, [itm_practice_staff]),
      (34, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield]),
      (35, mtef_visitor_source|mtef_team_4, af_override_all, aif_start_alarmed, 1, [itm_practice_staff]),
      (36, mtef_visitor_source|mtef_team_1, af_override_all, aif_start_alarmed, 1, [itm_practice_bow, itm_practice_arrows]),
      (37, mtef_visitor_source|mtef_team_2, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield]),
      (38, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword]),
      (39, mtef_visitor_source|mtef_team_4, af_override_all, aif_start_alarmed, 1, [itm_practice_staff]),
#40-49 not used yet
      (24, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_practice_bow, itm_practice_arrows, itm_practice_horse, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (24, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (24, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_practice_horse, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (24, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_practice_lance, itm_practice_shield, itm_practice_horse, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (24, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_practice_bow, itm_practice_arrows, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (24, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield, itm_arena_tunic_yellow]),
      (24, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_practice_horse, itm_arena_tunic_yellow]),
      (24, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_practice_lance, itm_practice_shield, itm_practice_horse, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (24, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_practice_bow, itm_practice_arrows, itm_practice_horse, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (24, mtef_visitor_source|mtef_team_3, af_override_all, aif_start_alarmed, 1, [itm_practice_bow, itm_practice_arrows, itm_practice_horse, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),

      (50, mtef_scene_source, af_override_horse|af_override_weapons|af_override_head, 0, 1, []),
      (51, mtef_visitor_source, af_override_horse|af_override_weapons|af_override_head, 0, 1, []),
      (52, mtef_scene_source, af_override_horse, 0, 1, []),
#not used yet:
      (53, mtef_scene_source, af_override_horse, 0, 1, []), (54, mtef_scene_source, af_override_horse, 0, 1, []), (55, mtef_scene_source, af_override_horse, 0, 1, []),
#used for torunament master scene

      (56, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield, itm_padded_cloth, itm_segmented_helmet]),
      (57, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield, itm_padded_cloth, itm_segmented_helmet]),
    ],
    tournament_triggers
  ),
]
