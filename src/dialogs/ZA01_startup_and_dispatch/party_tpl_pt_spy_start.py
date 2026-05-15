DIALOGS = [
[party_tpl|pt_spy, "start", [
   (check_quest_active, "qst_follow_spy"),
   (neg|check_quest_concluded, "qst_follow_spy"),
   (eq, "$qst_follow_spy_no_active_parties", 0),
   (eq, "$qst_follow_spy_spy_party", "$g_encountered_party"),
   (party_is_active, "$g_encountered_party"),
],
   "Good day, {sir/madam}. Fine weather for the road, is it not? I should be moving on.", "follow_spy_talk", []],
]
