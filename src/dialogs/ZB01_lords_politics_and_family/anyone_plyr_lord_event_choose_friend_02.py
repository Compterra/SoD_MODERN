DIALOGS = [
[anyone|plyr , "lord_event_choose_friend", [],  "{s6} is an honourable man, you've no right to speak of him thus.", "lord_event_choose_friend_defend", [
      (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -10),
      (call_script, "script_change_player_relation_with_troop", "$temp", 5),
      ]],
]
