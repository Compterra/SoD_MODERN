DIALOGS = [
[anyone|plyr , "lord_event_choose_friend", [],  "I don't want to be involved in your quarrel with {s6}.", "lord_event_choose_friend_neutral", [
      (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -2),
      (call_script, "script_change_player_relation_with_troop", "$temp", -3),
      ]],
]
