DIALOGS = [
[trp_seven_ash_garric_ashbow, "start",
    [
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_garric),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_garric_return_applied, 0),
      (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_garric_status, sod_seven_ash_recruit_recruited),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_garric_status, sod_seven_ash_recruit_alienated),
    ],
    "This platform is too proud of itself. The south notch is blind, the ladder is a death joke, and whoever stacked that barrel wants archers trapped behind their own cover. Give me six villagers and no speeches.",
    "seven_ash_garric_return_reply",
    []],
[trp_seven_ash_garric_ashbow|plyr, "seven_ash_garric_return_reply", [],
    "Take them. Teach them the difference between courage and wasting arrows.",
    "seven_ash_garric_return_done",
    []],
[trp_seven_ash_garric_ashbow, "seven_ash_garric_return_done", [],
    "Good. First lesson: if you cannot see a face, you do not shoot at a sound. Panic empties quivers faster than enemies do.",
    "close_window",
    [
      (call_script, "script_sod_seven_ash_apply_first_defender_return", sod_seven_ash_defender_garric),
    ]],
]
