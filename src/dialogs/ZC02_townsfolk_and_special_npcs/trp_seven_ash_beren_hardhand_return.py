DIALOGS = [
[trp_seven_ash_beren_hardhand, "start",
    [
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_beren),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_beren_return_applied, 0),
      (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_beren_status, sod_seven_ash_recruit_recruited),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_beren_status, sod_seven_ash_recruit_alienated),
    ],
    "Halvorn will not hit the strongest plank. He will hit where fear opens a gap. Put me there, but put someone behind me who knows the word stop.",
    "seven_ash_beren_return_reply",
    []],
[trp_seven_ash_beren_hardhand|plyr, "seven_ash_beren_return_reply", [],
    "You hold the breach. Mother Hilda names the stop. If you cannot hear her, you are no use to us.",
    "seven_ash_beren_return_done",
    []],
[trp_seven_ash_beren_hardhand, "seven_ash_beren_return_done", [],
    "Hah. A priest's voice as a leash. Fine. Better than pretending I came here tame.",
    "close_window",
    [
      (call_script, "script_sod_seven_ash_apply_first_defender_return", sod_seven_ash_defender_beren),
    ]],
]
