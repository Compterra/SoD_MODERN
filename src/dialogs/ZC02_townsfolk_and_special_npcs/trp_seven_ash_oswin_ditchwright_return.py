DIALOGS = [
[trp_seven_ash_oswin_ditchwright, "start",
    [
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_oswin),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_oswin_return_applied, 0),
      (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_oswin_status, sod_seven_ash_recruit_recruited),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_oswin_status, sod_seven_ash_recruit_alienated),
    ],
    "Your palisade leans like a drunk trying to look useful. I need the old cart shed, three roofs worth of straight timber, and someone brave enough to tell Piers his favorite gate is firewood now.",
    "seven_ash_oswin_return_reply",
    []],
[trp_seven_ash_oswin_ditchwright|plyr, "seven_ash_oswin_return_reply", [],
    "Take the timber. Leave us a gate that survives the first serious push.",
    "seven_ash_oswin_return_done",
    []],
[trp_seven_ash_oswin_ditchwright, "seven_ash_oswin_return_done", [],
    "Survives, yes. Flatters, no. Anyone who wants pretty wood can carve grave markers after.",
    "close_window",
    [
      (call_script, "script_sod_seven_ash_apply_first_defender_return", sod_seven_ash_defender_oswin),
    ]],
]
