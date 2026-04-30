DIALOGS = [
[anyone, "gm_tell_mission", [(eq, "$random_quest_no", "qst_conquistadors_collect_debt"),
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (call_script, "script_store_troop_name_link", s3, ":quest_target_troop"),],
   "One of the Vaegir lords, {s3} refused to pay for our services in a battle against the Swadians, and hasn't settled things with us ever since.  However, due to political issues it wouldn't be good for us to openly protest against his actions, but an 'outsider', like yourself, should have little problem asking him about it.  Should he still refuse, you can still challenge him to a duel.  If you defeat him fair and square, I'm fairly sure he'll pay the requested wage.  Afterwards, bring the wage to our camp.  I can offer a part of the owed money if you're willing to help, as well as our gratitude.", "gm_tell_mission_collect_debt_2",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, reg4, "$random_quest_no", slot_quest_target_amount),
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (call_script, "script_store_troop_name_link", s3, ":quest_target_troop"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to collect the debt of {reg4} denars {s3} owes to him."),
   ]],
]
