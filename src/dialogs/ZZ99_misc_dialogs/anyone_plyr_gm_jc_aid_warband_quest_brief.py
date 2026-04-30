DIALOGS = [
[anyone|plyr, "gm_jc_aid_warband_quest_brief", [],
   "Alright. I will help them.", "gm_merchant_quest_taken_bandits",
   [
	(quest_get_slot, ":quest_target_center", "qst_jotnar_clan_aid_warband", slot_quest_target_center),
	(set_spawn_radius, 2),
	(spawn_around_party, ":quest_target_center", "pt_jotnar_clan_warriors"),
	(party_set_ai_behavior, reg0, ai_bhvr_hold),
	(call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
	(setup_quest_text, "$random_quest_no"),
    (str_store_string, s2, "@{s9} asked you to help Jotnar Clan warriors garrisoned near {s8}."),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
]
