DIALOGS = [
[anyone|plyr, "prison_break_lord_talk_2", [
  (call_script, "script_succeed_quest", "qst_slave_q1"),
  (call_script, "script_end_quest", "qst_slave_q1"),
  (call_script, "script_change_player_relation_with_faction", "fac_commoners", 5),
  ], "What ? You abandon your friend, as simply as that ?", "prison_break_lord_talk_3", []],
]
