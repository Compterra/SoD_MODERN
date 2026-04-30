DIALOGS = [
[anyone|plyr, "mercenaries_talk", [
  ], "Defend yourself! [Attack]", "close_window", [
  (call_script, "script_change_player_relation_with_faction", "fac_manhunters", -5),
  ]],
]
