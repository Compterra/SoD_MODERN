DIALOGS = [
[anyone,
    "member_automanage_select_melee_1",
    [
      (call_script, "script_print_wpn_upgrades_to_s0", reg3),
      (str_store_string, s2, "@My weapon slot upgrades are as follows: {s0}")
    ],
    "{s2}^What would you like to change?",
    "member_automanage_select_melee",
    []
  ],
]
