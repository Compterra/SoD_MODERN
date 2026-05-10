DIALOGS = [
[trp_seven_ash_tomas_reed, "start",
    [
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_tomas),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_tomas_return_applied, 0),
      (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_tomas_status, sod_seven_ash_recruit_recruited),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_tomas_status, sod_seven_ash_recruit_alienated),
    ],
    "Good. No bad habits yet. They hold spears like broom handles, but broom handles can point the same way. Do I teach them to stand, or to hurt?",
    "seven_ash_tomas_return_reply",
    []],
[trp_seven_ash_tomas_reed|plyr, "seven_ash_tomas_return_reply", [],
    "Teach them to stand first. Hurting comes easily when fear has somewhere to put its feet.",
    "seven_ash_tomas_return_done",
    []],
[trp_seven_ash_tomas_reed, "seven_ash_tomas_return_done", [],
    "Then feet first, breath second, points third. If they remember that much when the shouting starts, Ashwick has soldiers enough for one hard hour.",
    "close_window",
    [
      (call_script, "script_sod_seven_ash_apply_first_defender_return", sod_seven_ash_defender_tomas),
    ]],
]
