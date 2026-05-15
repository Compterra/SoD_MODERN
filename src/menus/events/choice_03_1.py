MENUS = [
(
    "event_03", mnf_disable_all_keys,
    "A young noble has been spreading foul rumors about one of the ladies of your court. The accusation is crude, public, and dangerous enough to demand an answer.",
    "none",
    [

    ],
    [
      ("choice_03_1", [], "Challenge him to a duel.",
       [
    (assign, ":arena_scene", "scn_random_scene"),
    (try_begin),
      (assign, ":closest_dist", 100000),
      (assign, ":closest_town", -1),
      (try_for_range, ":cur_town", towns_begin, towns_end),
        (store_distance_to_party_from_party, ":dist", ":cur_town", "p_main_party"),
        (lt, ":dist", ":closest_dist"),
        (assign, ":closest_dist", ":dist"),
        (assign, ":closest_town", ":cur_town"),
      (try_end),
      (is_between, ":closest_town", towns_begin, towns_end),
      (party_get_slot, ":arena_scene", ":closest_town", slot_town_arena),
      (le, ":arena_scene", 0),
      (assign, ":arena_scene", "scn_random_scene"),
    (try_end),
    (set_jump_entry, 56),
    (modify_visitors_at_site, ":arena_scene"),
    (reset_visitors),
    (set_visitor, 56, "trp_player"),
    (set_visitor, 58, "trp_swadian_knight"),
    (set_jump_mission, "mt_sod_arena_duel_fight"),
    (jump_to_scene, ":arena_scene"),
	(change_screen_mission),
  #  (try_begin),
  #    (neq, "$talk_context", tc_court_talk),
   #   (jump_to_menu, "mnu_arena_duel_fight"),
  #  (try_end),
        ]
       ),
      ("choice_03_2", [], "This is a court quarrel. I will not intervene.",
       [
        (change_screen_return),
        ]
       ),
      ("choice_03_3", [(eq, "$character_gender", tf_male), (eq, "$g_sod_parental_advisory", 0)], "Arrange for him to meet with an accident.",
       [
       (call_script, "script_change_player_honor", -3),
       (change_screen_return),
        ]
       ),
      ]
  ),
]
