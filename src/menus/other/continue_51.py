MENUS = [
(
    "captivity_rescue_lord_taken_prisoner", 0,
    "You remain in disguise for as long as possible before revealing yourself. The guards are outraged and beat you savagely before throwing you back into the cell for God knows how long...",
    "none",
    [
        (troop_get_type, ":is_female", "trp_player"),
        (try_begin),
          (eq, ":is_female", 1),
          (set_background_mesh, "mesh_pic_prisoner_fem"),
        (else_try),
          (set_background_mesh, "mesh_pic_prisoner_man"),
        (try_end),
   ],
    [
      ("continue", [], "Continue...",
       [
           (assign, "$g_player_is_captive", 1),
           (store_random_in_range, ":random_hours", 16, 22),
           (call_script, "script_event_player_captured_as_prisoner"),
           (call_script, "script_stay_captive_for_hours", ":random_hours"),
           (assign, "$auto_menu", "mnu_captivity_castle_check"),
           (change_screen_return),
        ]),
    ]
  ),
]
