DIALOGS = [
[trp_seven_ash_sir_aldrik_vane, "start",
    [
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_aldrik),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_aldrik_return_applied, 0),
      (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_aldrik_status, sod_seven_ash_recruit_recruited),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_aldrik_status, sod_seven_ash_recruit_alienated),
    ],
    "If I place this shield here, they will cheer a story larger than I am. That can steady them. It can also lie to them. Do you still want it on the gate?",
    "seven_ash_aldrik_return_reply",
    []],
[trp_seven_ash_sir_aldrik_vane|plyr, "seven_ash_aldrik_return_reply", [],
    "Place it. Then teach them that an oath is work, not decoration.",
    "seven_ash_aldrik_return_done",
    []],
[trp_seven_ash_sir_aldrik_vane, "seven_ash_aldrik_return_done", [],
    "Good. Then I begin with the shieldmen, not the cheering. Hope without formation is only noise.",
    "close_window",
    [
      (call_script, "script_sod_seven_ash_apply_first_defender_return", sod_seven_ash_defender_aldrik),
    ]],
]
