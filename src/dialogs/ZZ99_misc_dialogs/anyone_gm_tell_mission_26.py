DIALOGS = [
[anyone, "gm_tell_mission", [(eq, "$random_quest_no", "qst_slavers_deliver_wine")],
   "{s3} asked us to deliver a supply of expensive wine to {s4}.  But you see, the local laws tax these kinds of luxury quite a bit, which he intends to avoid.  Since getting caught is likely if we employ our local colleges, I think we could use a 'third person' like you for this job if you're up to it...", "slavers_quest_brief_deliver_wine",
   [(quest_get_slot, reg5, "qst_slavers_deliver_wine", slot_quest_target_amount),
	(quest_get_slot, ":target_troop", "qst_slavers_deliver_wine", slot_quest_target_troop),
	(call_script, "script_store_troop_name_link", s3, ":target_troop"),
    (quest_get_slot, ":quest_target_center", "qst_slavers_deliver_wine", slot_quest_target_center),
    (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
    (str_store_party_name_link, s4, ":quest_target_center"),
	(str_store_party_name, s10, "$g_encountered_party"),
    (setup_quest_text, "qst_slavers_deliver_wine"),
    (str_store_string, s2, "@{s9} of {s10} asked you to smuggle {reg5} units of wine to {s4}."),
   ]],
]
