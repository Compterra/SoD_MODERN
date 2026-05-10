MENUS = [
("training_ground_selection_details_mounted", 0,
   "What kind of weapon do you want to train with?",
   "none",
   [],
    [
      ("camp_train_mounted_details_1", [], "One handed weapon.",
       [
         (call_script, "script_start_training_at_training_ground", itp_type_one_handed_wpn, 0),
         ]),
      ("camp_train_mounted_details_2", [], "Polearm.",
       [
         (call_script, "script_start_training_at_training_ground", itp_type_polearm, 0),
         ]),
      ("camp_train_mounted_details_3", [], "Bow.",
       [
         (call_script, "script_start_training_at_training_ground", itp_type_bow, 0),
         ]),
      ("camp_train_mounted_details_4", [], "Thrown weapon.",
       [
         (call_script, "script_start_training_at_training_ground", itp_type_thrown, 0),
         ]),
      ("go_back_dot", [], "Go back.",
       [(jump_to_menu, "mnu_training_ground"),
        ]
       ),
      ]
  ),
]
