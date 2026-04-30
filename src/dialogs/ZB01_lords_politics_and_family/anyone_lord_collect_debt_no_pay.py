DIALOGS = [
[anyone, "lord_collect_debt_no_pay", [], "Is this a joke?\
 I know full well that {s7} gave you the money, and I want every denar owed to me, {sir/madam}.\
 As far as I'm concerned, I hold you personally in my debt until I see that silver.", "close_window", [
     (call_script, "script_change_debt_to_troop", "$g_talk_troop", reg4),
     (call_script, "script_end_quest", "qst_collect_debt"),

     (call_script, "script_objectionable_action", tmt_honest, "str_squander_money"),
     ]],
]
