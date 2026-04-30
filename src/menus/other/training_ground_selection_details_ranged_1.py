MENUS = [
("training_ground_selection_details_ranged_1", 0,
   "What kind of ranged weapon do you want to train with?",
   "none",
   [],
    [
      ("camp_train_ranged_weapon_bow", [], "Bow and arrows.",
       [
         (assign, "$g_mt_mode", ctm_ranged),
         (assign, "$temp", itp_type_bow),
         (jump_to_menu, "mnu_training_ground_selection_details_ranged_2"),
         ]),
      ("camp_train_ranged_weapon_crossbow", [], "Crossbow.",
       [
         (assign, "$g_mt_mode", ctm_ranged),
         (assign, "$temp", itp_type_crossbow),
         (jump_to_menu, "mnu_training_ground_selection_details_ranged_2"),
         ]),
      ("camp_train_ranged_weapon_thrown", [], "Throwing Knives.",
       [
         (assign, "$g_mt_mode", ctm_ranged),
         (assign, "$temp", itp_type_thrown),
         (jump_to_menu, "mnu_training_ground_selection_details_ranged_2"),
         ]),
      ("go_back_dot", [], "Go back.",
       [(jump_to_menu, "mnu_training_ground"),
        ]
       ),
      ]
  ),
]
