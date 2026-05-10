MENUS = [
(
    "captivity_start_wilderness_defeat", 0,
    "Your enemies take you prisoner.",
    "none",
    [
       (assign, "$g_player_is_captive", 1),
       (assign, "$auto_menu", -1),
       (call_script, "script_sod_capture_set_capturer_from_encounter_to_reg"),
       (jump_to_menu, "mnu_captivity_wilderness_taken_prisoner"),
    ],
    []
  ),
]
