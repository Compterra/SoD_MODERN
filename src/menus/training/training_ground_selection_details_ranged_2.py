MENUS = [
("training_ground_selection_details_ranged_2", 0,
   "What range do you want to practice at?",
   "none",
   [],
    [
      ("camp_train_ranged_details_1", [], "10 yards.",
       [
         (call_script, "script_start_training_at_training_ground", "$temp", 10),
         ]),
      ("camp_train_ranged_details_2", [], "20 yards.",
       [
         (call_script, "script_start_training_at_training_ground", "$temp", 20),
         ]),
      ("camp_train_ranged_details_3", [], "30 yards.",
       [
         (call_script, "script_start_training_at_training_ground", "$temp", 30),
         ]),
      ("camp_train_ranged_details_4", [], "40 yards.",
       [
         (call_script, "script_start_training_at_training_ground", "$temp", 40),
         ]),
      ("camp_train_ranged_details_5", [(eq, "$g_mt_mode", ctm_ranged), ], "50 yards.",
       [
         (call_script, "script_start_training_at_training_ground", "$temp", 50),
         ]),
      ("camp_train_ranged_details_6", [(eq, "$g_mt_mode", ctm_ranged), ], "60 yards.",
       [
         (call_script, "script_start_training_at_training_ground", "$temp", 60),
         ]),
      ("camp_train_ranged_details_7", [(eq, "$g_mt_mode", ctm_ranged), ], "70 yards.",
       [
         (call_script, "script_start_training_at_training_ground", "$temp", 70),
         ]),
      ("go_back_dot", [], "Go back.",
       [(jump_to_menu, "mnu_training_ground"),
        ]
       ),
      ]
  ),
]
