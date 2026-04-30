DIALOGS = [
[anyone, "gm_tell_mission", [(eq, "$random_quest_no", "qst_black_army_collect_debt"),
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (call_script, "script_store_troop_name_link", s3, ":quest_target_troop"),],
   "We have an issue of late salary on our hands.  In the past, we saved {s3}'s sorry behind in battle and the pig still hasn't paid his dues.  Now, I believe you agree that it would look quite unpleasant if we, lowly mercenaries would pressure him with threatening letters or threatening-looking bouncers, so a third person would provide the quickest way to settle this little problem.  Seek out the guy and send him my greetings.  Hopefully he'll understand.  And I DO hope you won't get the idea of stepping off with the money once you have it, because I'll be in a VERY foul mood then.  Any questions? No?  Fine.  Then go!", "gm_tell_mission_collect_debt_2",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, reg4, "$random_quest_no", slot_quest_target_amount),
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (call_script, "script_store_troop_name_link", s3, ":quest_target_troop"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to collect the debt of {reg4} denars {s3} owes to him."),
   ]],
]
