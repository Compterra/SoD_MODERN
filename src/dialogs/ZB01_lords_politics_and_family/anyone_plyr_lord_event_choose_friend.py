DIALOGS = [
[anyone|plyr , "lord_event_choose_friend", [],  "I assure you, {s65}, I am no friend of {s6}.", "lord_event_choose_friend_renounce", [
      (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 5),
      (call_script, "script_change_player_relation_with_troop", "$temp", -10),
      ]],
]
