DIALOGS = [
[anyone|plyr , "lord_event_choose_friend", [],  "I will not lend my name to this quarrel with {s6}. Choose another witness for it.", "lord_event_choose_friend_neutral", [
      (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -2),
      (call_script, "script_change_player_relation_with_troop", "$temp", -3),
      ]],
]
