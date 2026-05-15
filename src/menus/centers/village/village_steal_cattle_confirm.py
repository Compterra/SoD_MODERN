MENUS = [
(
    "village_steal_cattle_confirm", 0,
    "{s68}",
    "none",
    [
      (call_script, "script_get_max_skill_of_player_party", "skl_looting"),
      (assign, reg2, reg0),
      (assign, ":max_skill_owner", reg1),
      (try_begin),
        (eq, ":max_skill_owner", "trp_player"),
        (assign, reg3, 1),
        (str_store_string, s68, "@You reckon the herd can be driven off, though confusion, darkness, and frightened villagers will decide how much you truly get away with."),
      (else_try),
        (assign, reg3, 0),
        (call_script, "script_store_troop_name", s1, ":max_skill_owner"),
        (str_store_string, s68, "@{s1} reckons the herd can be driven off, though confusion, darkness, and frightened villagers will decide how much you truly get away with."),
      (try_end),
      (call_script, "script_calculate_amount_of_cattle_can_be_stolen", "$current_town"),
      (assign, reg4, reg0),
      ],
    [
      ("village_steal_cattle_confirm", [], "Go on.",
       [
         (rest_for_hours_interactive, 3, 5, 1), #rest while attackable
         (assign, "$auto_menu", "mnu_village_steal_cattle"),
         (change_screen_return),
         ]),
      ("forget_it", [], "Forget it.", [(change_screen_return)]),
    ],
  ),
]
