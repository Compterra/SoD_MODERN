DIALOGS = [
[anyone,
    "member_automanage_select_melee_2",
    [
      (call_script, "script_print_wpn_upgrades_to_s0", reg3),
      (str_store_string_reg, s68, s0),
        (try_begin),
          (eq, reg1, 4),
          (str_store_string, s2, "@Is this satisfactory?"),
        (else_try),
          (str_store_string, s2, "@Select the type of item for slot {reg1}."),
        (try_end),
    ],
    "My current weapon upgrade settings are: {s68}^^{s2}",
    "member_automanage_select_melee_slot",
    []
  ],
]
