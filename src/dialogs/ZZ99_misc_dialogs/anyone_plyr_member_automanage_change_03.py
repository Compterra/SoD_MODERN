DIALOGS = [
[anyone|plyr,
    "member_automanage_change",
    [
      (troop_get_slot, reg4, reg3, slot_troop_upgrade_armor),
      (eq, reg4, 0)
    ],
    "Start upgrading your armour on your own.",
    "member_automanage_report",
    [
      (troop_set_slot, reg3, slot_troop_upgrade_armor, 1)
    ]
  ],
]
