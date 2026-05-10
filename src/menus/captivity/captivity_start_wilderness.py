MENUS = [
(
    "captivity_start_wilderness", 0,
    "You are captured in the wilderness.",
    "none",
    [
          (assign, "$g_player_is_captive", 1),
          (call_script, "script_sod_capture_set_capturer_from_encounter_to_reg"),
          (try_begin),
            (eq, "$g_player_surrenders", 1),
            (jump_to_menu, "mnu_captivity_start_wilderness_surrender"),
          (else_try),
            (jump_to_menu, "mnu_captivity_start_wilderness_defeat"),
          (try_end),
      ],
    []
  ),
]
