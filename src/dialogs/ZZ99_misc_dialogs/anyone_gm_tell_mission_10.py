DIALOGS = [
[anyone, "gm_tell_mission", [(eq, "$random_quest_no", "qst_slavers_collect_debt")],
   "{s3} owes a serious amount of money for us. In the past, he made use of our, ahem, talents to carry out a job concerning his mother-in-law but hasn't paid the requested wage ever since.  Sadly, we lack the influence in the area to enforce him to pay, thus we need an outsider for that purpose... but don't think of running away with the money once you have it, cos' we'll know it.  And you don't want that.  Trust me.", "gm_tell_mission_collect_debt",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, reg4, "$random_quest_no", slot_quest_target_amount),
	 (str_store_party_name, s10, "$g_encountered_party"),
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (call_script, "script_store_troop_name_link", s3, ":quest_target_troop"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} of {s10} asked you to collect the debt of {reg4} denars {s3} owes to him."),
   ]],
]
