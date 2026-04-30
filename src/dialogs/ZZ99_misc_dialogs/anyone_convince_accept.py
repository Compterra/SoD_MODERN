DIALOGS = [
[anyone, "convince_accept", [(call_script, "script_cf_prepare_collect_debt_acceptance", "$g_convince_quest", "$g_talk_troop")],
   "My debt to {s8} has long been overdue and was a source of great discomfort to me.\
 Thank you for accepting to take the money to him.\
 Please give him these {reg10} denars and thank him on my behalf.", "close_window",
   [(call_script, "script_troop_add_gold", "trp_player", reg10),
    (quest_set_slot,  "$g_convince_quest", slot_quest_current_state, 1),
    (call_script, "script_succeed_quest", "$g_convince_quest"),
    (assign, "$g_leave_encounter", 1),
    ]],
]
