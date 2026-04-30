DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_collect_debt")],
   "Some time ago, I loaned out a considerable sum of money to {s3}. {reg4} denars, to be precise.\
 He was supposed to pay it back within a month but I haven't received a copper from him since.\
 That was months ago. If you could collect the debt from him on my behalf,\
 I would be grateful indeed. I would even let you keep one fifth of the money for your trouble.\
 What do you say?", "lord_tell_mission_collect_debt",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, reg4, "$random_quest_no", slot_quest_target_amount),
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (call_script, "script_store_troop_name_link", s3, ":quest_target_troop"),
     (str_store_party_name_link, s4, ":quest_target_center"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to collect the debt of {reg4} denars owed by {s3}. {s3} was at {s4} when you were given this quest."),
   ]],
]
