DIALOGS = [
[anyone|plyr,
    "member_automanage_change",
    [
      (troop_get_slot, reg4, reg3, slot_troop_upgrade_armor),
      (neq, reg4, 0)
    ],
    "Stop upgrading armour.",
    "member_automanage_report",
    [
      (troop_set_slot, reg3, slot_troop_upgrade_armor, 0)
    ]
  ],
]
