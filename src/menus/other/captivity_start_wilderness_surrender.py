MENUS = [
(
    "captivity_start_wilderness_surrender", 0,
    "Stub",
    "none",
    [
       (assign, "$g_player_is_captive", 1),
       (assign, "$auto_menu", -1), #We need this since we may come here by something other than auto_menu
       (assign, "$capturer_party", "$g_encountered_party"),
       (jump_to_menu, "mnu_captivity_wilderness_taken_prisoner"),
      ],
    []
  ),
]
