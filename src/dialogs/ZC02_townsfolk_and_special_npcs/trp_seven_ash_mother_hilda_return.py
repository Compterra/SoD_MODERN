DIALOGS = [
[trp_seven_ash_mother_hilda, "start",
    [
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_complete, 1),
      (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act3_pressure_started, 0),
    ],
    "I need beds for the ones you brought and names for the ones you did not. Reeve Martin wants to know how much grain buys another week. Nell wants to know whether the road behind you is empty because you were quick, or because Wulfred was quicker.",
    "seven_ash_return_hilda_reply",
    []],
[trp_seven_ash_mother_hilda|plyr, "seven_ash_return_hilda_reply", [],
    "Count the beds, count the grain, and ring the village in. The search is over. Now Ashwick learns fear together.",
    "seven_ash_return_hilda_done",
    []],
[trp_seven_ash_mother_hilda, "seven_ash_return_hilda_done", [],
    "Then I will tell them the truth with no polish on it. Hope can survive plain speech. It rarely survives being sold dear.",
    "close_window",
    [
      (call_script, "script_sod_seven_ash_begin_act3_return"),
    ]],
]
