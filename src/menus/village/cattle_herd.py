MENUS = [
("cattle_herd", mnf_scale_picture,
   "You encounter a herd of cattle.",
   "none",
   [(play_sound, "snd_cow_moo"),
    (set_background_mesh, "mesh_pic_cattle"),
   ],
    [
      ("cattle_drive_away", [], "Drive the cattle onward.",
       [
        (party_set_slot, "$g_encountered_party", slot_cattle_driven_by_player, 1),
        (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_driven_by_party),
        (party_set_ai_object, "$g_encountered_party", "p_main_party"),
        (change_screen_return),
        ]
       ),
      ("cattle_stop", [], "Bring the herd to a stop.",
       [
        (party_set_slot, "$g_encountered_party", slot_cattle_driven_by_player, 0),
        (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_hold),
        (change_screen_return),
        ]
       ),
      ("cattle_kill", [(assign, ":continue", 1),
                      (try_begin),
                        (check_quest_active, "qst_move_cattle_herd"),
                        (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, "$g_encountered_party"),
                        (assign, ":continue", 0),
                      (try_end),
                      (eq, ":continue", 1)], "Slaughter some of the animals.",
       [(jump_to_menu, "mnu_cattle_herd_kill"),
        ]
       ),
      ("leave", [], "Leave.",
       [(change_screen_return),
        ]
       ),
      ]
  ),
]
