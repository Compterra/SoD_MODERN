DIALOGS = [
[anyone,
    "member_automanage_report",
    [
      (store_conversation_troop, reg3),
      (call_script, "script_print_wpn_upgrades_to_s0", reg3),
      (str_store_string, s2, "@My weapon slot upgrades are as follows: {s0}"),
      (troop_get_slot, reg4, reg3, slot_troop_upgrade_armor),
      (val_add, reg4, "str_hero_not_upgrading_armor"),
      (str_store_string, 1, reg4),
      (troop_get_slot, reg4, reg3, slot_troop_upgrade_horse),
      (val_add, reg4, "str_hero_not_upgrading_horse"),
      (str_store_string, 4, reg4)
    ],
    "I'm currently {s1} and {s4}. {s2}",
    "member_automanage_change",
    []
  ],
]
