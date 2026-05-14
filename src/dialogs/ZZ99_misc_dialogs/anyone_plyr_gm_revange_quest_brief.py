DIALOGS = [
[anyone|plyr, "gm_revange_quest_brief", [],
   "I will help them settle the account in blood and witnesses.", "gm_merchant_quest_taken_bandits",
   [
	(quest_get_slot, ":quest_target_center", "qst_jotnar_clan_revenge", slot_quest_target_center),
	(quest_get_slot, ":quest_target_troop", "qst_jotnar_clan_revenge", slot_quest_target_troop),
	(party_set_slot, ":quest_target_center", slot_village_infested_by_bandits, ":quest_target_troop"),
	(call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
	(party_add_template, "p_main_party", "pt_jotnar_revenge"),
	(setup_quest_text, "$random_quest_no"),
    (str_store_string, s2, "@{s9} asked you to help Disirs and Einherjars in their revenge on {s5} resting in {s8}."),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
]
