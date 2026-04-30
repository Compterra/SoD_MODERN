DIALOGS = [
[anyone|plyr,
    "member_automanage_change",
    [
      (troop_get_slot, reg4, reg3, slot_troop_upgrade_horse),
      (neq, reg4, 1)
    ],
    "Start upgrading your horse on your own.",
    "member_automanage_report",
    [
      (troop_set_slot, reg3, slot_troop_upgrade_horse, 1)
    ]
  ],
]
