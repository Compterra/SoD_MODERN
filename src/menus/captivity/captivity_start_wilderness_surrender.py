MENUS = [
(
    "captivity_start_wilderness_surrender", 0,
    "You lay down your arms in the wilderness and are taken prisoner.",
    "none",
    [
       (assign, "$g_player_is_captive", 1),
       (assign, "$auto_menu", -1), #We need this since we may come here by something other than auto_menu
       (call_script, "script_sod_capture_set_capturer_from_encounter_to_reg"),
       (jump_to_menu, "mnu_captivity_wilderness_taken_prisoner"),
      ],
    []
  ),
]
