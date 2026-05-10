DIALOGS = [
[trp_seven_ash_mirelle_voss, "start",
    [
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_mirelle),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_mirelle_return_applied, 0),
      (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_mirelle_status, sod_seven_ash_recruit_recruited),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_mirelle_status, sod_seven_ash_recruit_alienated),
    ],
    "Three women can keep a secret if you give each a different reason. This one thinks of her sons, this one of her goats, this one of the neighbor she hates enough to save. Do you want the routes marked for families or fighters?",
    "seven_ash_mirelle_return_reply",
    []],
[trp_seven_ash_mirelle_voss|plyr, "seven_ash_mirelle_return_reply", [],
    "Families first. Fighters can read smoke and shouting. Children need a hand on a latch.",
    "seven_ash_mirelle_return_done",
    []],
[trp_seven_ash_mirelle_voss, "seven_ash_mirelle_return_done", [],
    "Then the chalk marks go low where small eyes can find them, and the thread goes where frightened hands will brush it. A good exit is a lie told to panic before panic arrives.",
    "close_window",
    [
      (call_script, "script_sod_seven_ash_apply_first_defender_return", sod_seven_ash_defender_mirelle),
    ]],
]
