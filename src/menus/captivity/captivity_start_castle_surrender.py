MENUS = [
(
    "captivity_start_castle_surrender", 0,
    "You surrender and are taken prisoner.",
    "none",
    [
       (assign, "$g_player_is_captive", 1),
       (assign, "$auto_menu", -1),
       (call_script, "script_sod_capture_set_capturer_from_encounter_to_reg"),
       (jump_to_menu, "mnu_captivity_castle_taken_prisoner"),
      ],
    []
  ),
]
