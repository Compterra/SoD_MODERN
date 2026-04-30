DIALOGS = [
[anyone|plyr, "lady_qst_duel_for_lady_succeeded_1", [], "Please, {s65}, no reward is necessary.", "lady_qst_duel_for_lady_succeeded_2", [
  (str_store_string, s10, "@{playername}, what a dear {man/woman} you are,\
 but I will not allow you to refuse this. I owe you far more than I can say,\
 and I am sure you can put this money to far better use than I."),
    (call_script, "script_change_player_honor", 2),
  ]],
]
