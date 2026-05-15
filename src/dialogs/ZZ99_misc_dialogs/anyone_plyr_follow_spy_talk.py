DIALOGS = [
[anyone|plyr, "follow_spy_talk",
   [
     (check_quest_active, "qst_follow_spy"),
     (neg|check_quest_concluded, "qst_follow_spy"),
     (eq, "$qst_follow_spy_spy_party", "$g_encountered_party"),
     (party_is_active, "$g_encountered_party"),
     (quest_get_slot, ":quest_giver", "qst_follow_spy", slot_quest_giver_troop),
     (call_script, "script_store_troop_name", s1, ":quest_giver"),
     ],
   "In the name of {s1}, you are under arrest!", "follow_spy_talk_2", []],
]
