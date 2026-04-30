MENUS = [
(
    "captivity_start_under_siege_defeat", 0,
    "Your enemies take you prisoner.",
    "none",
    [
       (assign, "$g_player_is_captive", 1),
       (assign, "$auto_menu", -1),
       (assign, "$capturer_party", "$g_encountered_party"),
       (jump_to_menu, "mnu_captivity_castle_taken_prisoner"),
    ],
    []
  ),
]
