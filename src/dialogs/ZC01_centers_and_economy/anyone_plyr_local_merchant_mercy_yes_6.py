DIALOGS = [
[anyone|plyr, "local_merchant_mercy_yes_6", [], "Good. Go now, before I change my mind.", "close_window",
   [(quest_set_slot, "qst_kill_local_merchant", slot_quest_current_state, 2),
    (call_script, "script_succeed_quest", "qst_kill_local_merchant"),
    (finish_mission),
    ]],
]
