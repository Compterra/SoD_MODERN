MENUS = [
(
    "train_peasants_against_bandits", 0,
    "{s68}",
    "none",
    [(call_script, "script_get_max_skill_of_player_party", "skl_trainer"),
     (assign, ":max_skill", reg0),
     (assign, reg2, reg0),
     (assign, ":max_skill_owner", reg1),
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (call_script, "script_store_troop_name", s1, ":max_skill_owner"),
     (try_end),
     (store_sub, ":needed_hours", 20, ":max_skill"),
     (val_mul, ":needed_hours", 3),
     (val_div, ":needed_hours", 5),
     (store_sub, reg4, ":needed_hours", "$qst_train_peasants_against_bandits_num_hours_trained"),
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (str_store_string, s68, "@As the party member with the highest training skill ({reg2}), you expect that getting some peasants ready for practice will take {reg4} hours."),
     (else_try),
       (str_store_string, s68, "@As the party member with the highest training skill ({reg2}), {s1} expects that getting some peasants ready for practice will take {reg4} hours."),
     (try_end),
     ],
    [
      ("make_preparation", [], "Train them.",
       [
         (assign, "$qst_train_peasants_against_bandits_currently_training", 1),
         (rest_for_hours_interactive, 1000, 5, 0), #rest while not attackable
         (assign, "$auto_enter_town", "$current_town"),
         (assign, "$g_town_visit_after_rest", 1),
         (change_screen_return),
         ]),
      ("train_later", [], "Put it off until later.",
       [
         (jump_to_menu, "mnu_village"),
        ]),
    ]
  ),
]
