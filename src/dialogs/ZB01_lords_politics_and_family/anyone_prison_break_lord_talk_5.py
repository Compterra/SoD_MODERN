DIALOGS = [
[anyone, "prison_break_lord_talk_5", [
  (call_script, "script_store_troop_name_link", s13, "$g_talk_troop"),
  (setup_quest_text, "qst_slave_q2"),
  (str_store_string, s2, "@The lord you spoke with refused to help Diego directly. Return to Diego with the bad news."),
  (assign, "$prison_break", 2),
  (call_script, "script_start_quest", "qst_slave_q2", "$g_talk_troop"),
  ], "If I were to free him, I could endanger myself and my family as well. If you pity him so much, you'll have to free him yourself. If you do, I'll pull some strings so the Slavers won't bother you afterward, but that's all I can do. Now please depart and send word to Diego of our conversation.", "close_window", [(assign, "$g_leave_encounter", 1),]],
]