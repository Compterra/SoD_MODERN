MENUS = [
(
    "training_ground", 0,
    "You approach a training field where you can practice your martial skills. What kind of training do you want to do?",
    "none",
    [
      (store_add, "$g_training_ground_melee_training_scene", "scn_training_ground_ranged_melee_1", "$g_encountered_party"),
      (val_sub, "$g_training_ground_melee_training_scene", training_grounds_begin),
      (try_begin),
        (ge, "$g_training_ground_training_count", 3),
        (assign, "$g_training_ground_training_count", 0),
        (rest_for_hours, 1, 5, 1), #rest while attackable
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
      (try_end),
      ],
    [
      ("camp_trainer",
       [], "Speak with the trainer.",
       [
         (set_jump_mission, "mt_training_ground_trainer_talk"),
         (modify_visitors_at_site, "$g_training_ground_melee_training_scene"),
         (reset_visitors),
         (set_jump_entry, 5),
         (jump_to_scene, "$g_training_ground_melee_training_scene"),
         (change_screen_mission),
         (music_set_situation, 0),
         ]),
      ("camp_train_melee",
       [
         (neg|troop_is_wounded, "trp_player"),
         (call_script, "script_party_count_fit_for_battle", "p_main_party"),
         (gt, reg0, 1),
         ], "Sparring practice.",
       [
         (assign, "$g_mt_mode", ctm_melee),
         (jump_to_menu, "mnu_training_ground_selection_details_melee_1"),
         (music_set_situation, 0),
         ]),
      ("camp_train_archery", [], "Ranged weapon practice.",
       [
         (jump_to_menu, "mnu_training_ground_selection_details_ranged_1"),
         (music_set_situation, 0),
         ]),
      ("camp_train_mounted", [], "Horseback practice.",
       [
         (assign, "$g_mt_mode", ctm_mounted),
         (jump_to_menu, "mnu_training_ground_selection_details_mounted"),
         (music_set_situation, 0),
         ]),
      ("leave", [], "Leave.",
       [(change_screen_return),
        ]),
    ]
  ),
]
