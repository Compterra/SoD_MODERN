MENUS = [
("duel_menu", 0,
   "{s1}{s2}",
   "none",
   [
     (call_script, "script_sod_custom_lord_duel_describe_to_s1", "$g_sod_custom_duel_target"),
   ],
   [
     ("start_fight", [(call_script, "script_cf_sod_custom_lord_duel_can_start", "$g_sod_custom_duel_target")],
      "Start the duel.",
      [
        (call_script, "script_sod_custom_lord_duel_start", "$g_sod_custom_duel_target"),
      ]),
     ("daily_limit", [(call_script, "script_cf_sod_valid_lord_duel_target", "$g_sod_custom_duel_target"),
                      (call_script, "script_sod_custom_lord_duel_reset_daily_if_needed", "$g_sod_custom_duel_target"),
                      (troop_get_slot, ":duel_daily", "$g_sod_custom_duel_target", slot_troop_duel_daily),
                      (ge, ":duel_daily", duel_daily_limit),
                     ],
      "You have reached today's duel limit with this lord.",
      [
        (display_message, "@This lord has had enough formal duels for today.", warning_color),
        (jump_to_menu, "mnu_duel_menu"),
      ]),
     ("invalid_target", [(neg|call_script, "script_cf_sod_valid_lord_duel_target", "$g_sod_custom_duel_target")],
      "The duel cannot be arranged.",
      [
        (display_message, "@The challenged lord is no longer available.", warning_color),
        (change_screen_map),
      ]),
     ("leave", [], "Leave.",
      [
        (assign, "$g_sod_custom_duel_result", 0),
        (change_screen_map),
      ]),
   ]),
]
