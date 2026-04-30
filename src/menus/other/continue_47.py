MENUS = [
(
    "sneak_into_town_caught_ran_away", 0,
    "You make your way back through the gates and quickly retreat to the safety of the hills.",
    "none",
    [
      (set_background_mesh, "$g_sod_town_background"),
    ],
    [
      ("continue", [], "Continue...",
        [
          (assign, "$auto_menu", -1),
          (store_encountered_party, "$last_sneak_attempt_town"),
          (store_current_hours, "$last_sneak_attempt_time"),
          (change_screen_return),
        ]
      ),
    ]
  ),
]
