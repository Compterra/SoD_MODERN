DIALOGS = [
[party_tpl|pt_spy_partners, "start", [
   (check_quest_active, "qst_follow_spy"),
   (neg|check_quest_concluded, "qst_follow_spy"),
   (eq, "$qst_follow_spy_no_active_parties", 0),
   (eq, "$qst_follow_spy_spy_partners_party", "$g_encountered_party"),
   (party_is_active, "$g_encountered_party"),
],
   "Evening, traveler. Keep to your own road.", "spy_partners_talk", []],
]
