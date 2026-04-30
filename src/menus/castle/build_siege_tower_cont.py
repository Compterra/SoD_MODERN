MENUS = [
(
    "construct_siege_tower", mnf_enable_hot_keys,
    "As the party member with the highest Engineer skill ({reg2}), {reg3?you estimate:{s3} estimates} that building a siege tower will take {reg4} hours.",
    "none",
    [
      (set_background_mesh, "mesh_pic_construction"),

      (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
      (assign, ":max_skill", reg0),
      (assign, ":max_skill_owner", reg1),
      (assign, reg2, ":max_skill"),

      #MORDACHAI - reduce the time it takes to build a siege tower, and increase the effectiveness of engineering skill
      (store_sub, reg4, 12, ":max_skill"),
      (val_mul, reg4, 3),

      (try_begin),
        (eq, ":max_skill_owner", "trp_player"),
        (assign, reg3, 1),
      (else_try),
        (assign, reg3, 0),
        (call_script, "script_store_troop_name", s3, ":max_skill_owner"),
      (try_end),
    ],
    [
      ("build_siege_tower_cont", [],
       "Start building.", [
           (assign, "$g_siege_method", 2),
           (store_current_hours, ":cur_hours"),
           (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
           #MORDACHAI - reduce the time it takes to build a siege tower, and increase the effectiveness of engineering skill
           (store_sub, ":hours_takes", 12, reg0),
           (val_mul, ":hours_takes", 3),
           (store_add, "$g_siege_method_finish_hours", ":cur_hours", ":hours_takes"),
           (assign, "$auto_besiege_town", "$current_town"),
           (rest_for_hours_interactive, 240, 5, 1), #rest while attackable. A trigger will divert control when attack is ready.
           (change_screen_return),
           ]),
      ("go_back", [],
       "Go back.", [(jump_to_menu, "mnu_castle_besiege")]),
        ],
  ),
]
