DIALOGS = [
[anyone|plyr, "mercenaries_no_money_continue", [
  ], "You're not going anywhere! Defend yourself!", "close_window", [
  (call_script, "script_change_player_relation_with_faction", "fac_manhunters", -5),
  ]],
]
