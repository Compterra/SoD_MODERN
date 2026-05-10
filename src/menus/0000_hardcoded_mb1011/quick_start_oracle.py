MENUS = [
("quick_start_oracle", mnf_scale_picture|mnf_enable_hot_keys,
   "{s1}",
   "none",
   [
    (set_background_mesh, "mesh_pic_payment"),
    (store_current_day, ":today"),
    (store_sub, ":days_left", "$g_sod_invasion_begin", ":today"),
    (try_begin),
      (lt, ":today", "$g_sod_invasion_begin"),
      (try_begin),
        (le, ":days_left", 20),
        (str_store_string, s1, "@The invasion is close enough to taste iron in the wind..."),
      (else_try),
        (le, ":days_left", 60),
        (str_store_string, s1, "@The invasion is not immediate, but the road to it is short..."),
      (else_try),
        (str_store_string, s1, "@The invasion is still distant enough for preparation, if you do not waste the warning..."),
      (try_end),
      (assign, reg9, 0),
    (else_try),
      (str_store_string, s1, "@It has already begun! Dun, dun, dun!"),
      (assign, reg9, 1),
    (try_end),
   ],
   [
    ("invade_sooner", [(store_current_day, ":today"), (lt, ":today", "$g_sod_invasion_begin")],
      "That's too far away!  Make it sooner.",
      [
        (val_sub, "$g_sod_invasion_begin", 30),
        (store_current_day, ":today"),
        (store_add, ":tomorrow", ":today", 1),
        (val_max, "$g_sod_invasion_begin", ":tomorrow"),
      ]),

    ("invade_later", [(store_current_day, ":today"), (lt, ":today", "$g_sod_invasion_begin")],
      "What?!  I'm not nearly ready yet!  Make it later.",
      [(val_add, "$g_sod_invasion_begin", 30), (val_add, "$g_sod_cheat_mode_used", 1)]),

    ("invade_done", [(store_current_day, ":today"), (lt, ":today", "$g_sod_invasion_begin")],
      "I must return to my prepartions...",
      [(jump_to_menu, "mnu_quick_start")]),

    ("invade_too_late", [(store_current_day, ":today"), (ge, ":today", "$g_sod_invasion_begin")],
      "I knew that!", [(jump_to_menu, "mnu_quick_start")]),
   ]
  ),
]
