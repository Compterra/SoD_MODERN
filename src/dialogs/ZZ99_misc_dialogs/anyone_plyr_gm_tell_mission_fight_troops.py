DIALOGS = [
[anyone|plyr, "gm_tell_mission_fight_troops", [
  (quest_get_slot, ":message_text", "$random_quest_no", slot_quest_yes),
  (str_store_string, s15, ":message_text"),
  ], "{s15}", "gm_mission_fight_troops_accepted", [
     (setup_quest_text, "$random_quest_no"),
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (str_store_string, s2, "@{s9} invited you to join his guild troops training."),
	 (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
  ]],
]
