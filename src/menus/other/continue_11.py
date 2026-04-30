MENUS = [
(
    "castle_entry_denied", mnf_enable_hot_keys,
    "The lord of this castle has forbidden you from coming inside these walls, and the guard sergeant informs you that his men will fire if you attempt to come any closer.",
    "none",
    [
      (set_background_mesh, "$g_sod_town_background"),
    ],
    [
      ("continue", [],
       "Continue...",
       [(jump_to_menu, "mnu_castle_guard")]),
    ]
  ),
]
