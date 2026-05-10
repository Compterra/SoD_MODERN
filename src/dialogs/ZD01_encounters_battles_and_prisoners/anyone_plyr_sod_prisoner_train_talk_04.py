DIALOGS = [
[anyone|plyr, "sod_prisoner_train_talk", [
    (call_script, "script_sod_prisoner_train_quote_buy_price", "$g_encountered_party"),
    (eq, reg0, 1),
  ], "Your guards look tired. I will pay {reg1} denars to take {reg2} captives off your hands.", "close_window", [
    (call_script, "script_sod_player_buy_prisoners_from_train", "$g_encountered_party"),
    (assign, reg5, reg0),
    (assign, reg6, reg1),
    (display_message, "@You bought {reg5} captives from the prisoner train for {reg6} denars.", 0x99CCFF),
    (assign, "$g_leave_encounter", 1),
  ]],
]
