DIALOGS = [
[anyone|plyr,
    "member_automanage_change",
    [
      (troop_get_slot, reg4, reg3, slot_troop_upgrade_horse),
      (neq, reg4, 0)
    ],
    "Stop acquiring new horses.",
    "member_automanage_report",
    [
      (troop_set_slot, reg3, slot_troop_upgrade_horse, 0)
    ]
  ],
]
