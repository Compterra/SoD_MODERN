DIALOGS = [
[anyone, "gm_tell_mission_raise_troops_2", [], "If you could recruit {reg1} {s13} to our company, you may earn our gratitude and respect.", "gm_mission_raise_troops_told",
   [
     (quest_get_slot, reg1, "$random_quest_no", slot_quest_target_amount),
	 (quest_get_slot, ":quest_troop", "$random_quest_no", slot_quest_target_troop),
	 (str_store_troop_name_plural, s13, ":quest_troop"),
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to recruit and raise {reg1} {s13} and bring them to him."),
   ]],
]
