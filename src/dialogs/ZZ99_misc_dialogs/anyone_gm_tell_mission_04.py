DIALOGS = [
[anyone, "gm_tell_mission", [
  (this_or_next|eq, "$random_quest_no", "qst_elephant_guard_hunt_down_fugitive"),
  (this_or_next|eq, "$random_quest_no", "qst_bc_hunt_down_fugitive"),
  (eq, "$random_quest_no", "qst_conquistadors_hunt_down_fugitive"),
  (faction_get_slot, ":message_text", "$g_talk_troop_faction", slot_guild_fugitive_text),
  (quest_get_slot, ":quest_target_dna", "qst_elephant_guard_hunt_down_fugitive", slot_quest_target_dna),
  (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
  (str_store_string, s4, s50),
  (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
  (str_store_party_name_link, s3, ":quest_target_center"),
  (str_store_string, s15, ":message_text"),
  ],
   "{s15}", "gm_mission_hunt_down_fugitive_told",
   [
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to hunt down {s4}. He is currently believed to be at {s3}."),
   ]],
]
