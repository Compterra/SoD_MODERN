DIALOGS = [
[anyone|plyr, "lady_qst_duel_for_lady_succeeded_1", [], "{s66}, this is far too much!", "lady_qst_duel_for_lady_succeeded_2", [
  (str_store_string, s10, "@Forgive me, {playername}, but I must insist you accept it.\
 The money means little to me, and I owe you so much.\
 Here, take it, and let us speak no more of this."),
    (call_script, "script_change_player_honor", 1),
  ]],
]
