DIALOGS = [
[anyone|plyr, "follow_spy_talk",
   [
     (quest_get_slot, ":quest_giver", "qst_follow_spy", slot_quest_giver_troop),
     (call_script, "script_store_troop_name", s1, ":quest_giver"),
     ],
   "In the name of {s1}, you are under arrest!", "follow_spy_talk_2", []],
]
