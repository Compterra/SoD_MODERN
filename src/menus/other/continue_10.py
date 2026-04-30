MENUS = [
(
    "castle_entry_granted", mnf_enable_hot_keys,
    "After a brief wait, the guards open the gates for you and allow your party inside.",
    "none",
    [
      (set_background_mesh, "$g_sod_town_background"),
    ],
    [
      ("continue", [],
       "Continue...",
       [(jump_to_menu, "mnu_town")]),
    ]
  ),
]
