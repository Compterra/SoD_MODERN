MENUS = [
(
    "village_jotnar_clan_result", mnf_scale_picture,
    "{s9}",
    "none",
    [(try_begin),
       (eq, "$g_battle_result", 1),
       (call_script, "script_succeed_quest", "qst_jotnar_clan_aid_warband"),
	   (change_screen_map),
     (else_try),
       (str_store_string, s9, "@Try as you might, you could not defeat the enemy."),
     (try_end),
    ],
    [
      ("continue", [], "Continue...",
       [(call_script, "script_fail_quest", "qst_jotnar_clan_aid_warband"),
        (change_screen_map), ]),
    ],
  ),
]
