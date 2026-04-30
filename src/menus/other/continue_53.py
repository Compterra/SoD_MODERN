MENUS = [
(
    "captivity_castle_remain", mnf_scale_picture|mnf_disable_all_keys,
    "More days pass in the darkness of your cell. You get through them as best you can, enduring the kicks and curses of the guards, watching your underfed body waste away more and more...",
    "none",
    [
        (troop_get_type, ":is_female", "trp_player"),
        (try_begin),
          (eq, ":is_female", 1),
          (set_background_mesh, "mesh_pic_prisoner_fem"),
        (else_try),
          (set_background_mesh, "mesh_pic_prisoner_man"),
        (try_end),
        (store_random_in_range, ":random_hours", 16, 22),
        (call_script, "script_stay_captive_for_hours", ":random_hours"),
        (assign, "$auto_menu", "mnu_captivity_castle_check"),

    ],
    [
      ("continue", [], "Continue...",
       [
           (assign, "$g_player_is_captive", 1),
           (change_screen_return),
        ]),
    ]
  ),
]
