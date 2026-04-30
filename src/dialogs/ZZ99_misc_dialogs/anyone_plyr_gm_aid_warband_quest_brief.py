DIALOGS = [
[anyone|plyr, "gm_aid_warband_quest_brief", [],
   "Alright. I will help them.", "gm_merchant_quest_taken_bandits",
   [
	(quest_get_slot, ":quest_target_center", "qst_black_army_aid_warband", slot_quest_target_center),
	(quest_get_slot, ":quest_target_troop", "qst_black_army_aid_warband", slot_quest_target_troop),
	(party_set_slot, ":quest_target_center", slot_village_infested_by_bandits, ":quest_target_troop"),
	(call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
	(setup_quest_text, "$random_quest_no"),
    (str_store_string, s2, "@{s9} asked you to help Black Army warband garrisoned in {s8}."),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
]
