MISSION_TEMPLATES = [
(
    "back_alley_revolt", mtf_battle_mode, charge,
    "You lead your men to battle.",
    [(0, mtef_team_0|mtef_use_exact_number, af_override_horse|af_override_weapons|af_override_head, aif_start_alarmed, 4, [itm_quarter_staff]),
     (3, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
     ],
    [
      common_inventory_not_available,

      (ti_tab_pressed, 0, 0, [],
       [(question_box, "str_do_you_want_to_retreat"),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1, ":answer"),
        (eq, ":answer", 0),
        (jump_to_menu, "mnu_collect_taxes_failed"),
        (finish_mission), ]),

      (ti_tab_pressed, 0, 0, [(display_message, "@Cannot leave now.", red)], []),
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_fight),
         ]),

      (1, 4, ti_once, [(this_or_next|main_hero_fallen), (num_active_teams_le, 1)],
       [
           (try_begin),
             (main_hero_fallen),
             (jump_to_menu, "mnu_collect_taxes_failed"),
           (else_try),
             (jump_to_menu, "mnu_collect_taxes_rebels_killed"),
           (try_end),
           (finish_mission),
           ]),

      formations_init_kill_count,
      formations_update_kill_count,

    ],
  ),
]
