DIALOGS = [
[trp_seven_ash_sister_elianor, "start",
    [
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_elianor),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_elianor_return_applied, 0),
      (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_elianor_status, sod_seven_ash_recruit_recruited),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_elianor_status, sod_seven_ash_recruit_alienated),
    ],
    "I need the church key, the granary tally, and every cellar that stays dry. Mother Hilda has already agreed. I am asking you because the wounded will blame the person who says no.",
    "seven_ash_elianor_return_reply",
    []],
[trp_seven_ash_sister_elianor|plyr, "seven_ash_elianor_return_reply", [],
    "Take them. Make the church an infirmary before the battle teaches us how late we are.",
    "seven_ash_elianor_return_done",
    []],
[trp_seven_ash_sister_elianor, "seven_ash_elianor_return_done", [],
    "Good. Mercy is slower when it has to clear furniture first.",
    "close_window",
    [
      (call_script, "script_sod_seven_ash_apply_first_defender_return", sod_seven_ash_defender_elianor),
    ]],
]
