DIALOGS = [
[anyone|plyr,
    "member_automanage_select_melee_slot",
    [
      (neq, reg1, 4),
      (store_add, ":type", 10, "str_hero_wpn_slot_none"),
      (str_store_string, s68, ":type")
    ],
    "{s68}",
    "member_automanage_select_melee_2",
    [
      (store_add, ":slot_num", reg1, slot_troop_upgrade_wpn_0),
      (troop_set_slot, reg3, ":slot_num", 10),
      (val_add, reg1, 1)
    ]
  ],
]
