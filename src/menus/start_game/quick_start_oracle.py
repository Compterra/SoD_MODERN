MENUS = [
("quick_start_oracle", mnf_scale_picture|mnf_enable_hot_keys,
   "{s1}",
   "none",
   [
    (set_background_mesh, "mesh_pic_payment"),
    (assign, reg1, "$g_sod_invasion_begin"),
    (store_current_day, ":today"),
    (store_sub, reg2, reg1, ":today"),
    (try_begin),
      (lt, ":today", "$g_sod_invasion_begin"),
      (str_store_string, s1, "@The invasion won't happen until day {reg1}, which is {reg2} days from now..."),
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
