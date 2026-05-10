MENUS = [
(
    "village_take_food_confirm", 0,
    "It will be difficult to force and threaten the peasants into giving up their precious supplies. Your hardest hands know the work, but even a brutal search will take at least one hour.",
    "none",
    [
        (call_script, "script_get_max_skill_of_player_party", "skl_looting"),
        (assign, reg5, reg0),
    ],
    [
      ("village_take_food_confirm", [], "Go ahead.",
       [
         (call_script, "script_sod_companion_apply_player_action", sod_companion_action_abuse_village, 2),
         (rest_for_hours_interactive, 1, 5, 0), #rest while not attackable
         (assign, "$auto_enter_town", "$current_town"),
         (assign, "$g_town_visit_after_rest", 1),
         (assign, "$auto_enter_menu_in_center", "mnu_village_take_food"),
         (change_screen_return),
         ]),
      ("forget_it", [], "Forget it.", [(jump_to_menu, "mnu_village_hostile_action")]),
    ],
  ),
]
