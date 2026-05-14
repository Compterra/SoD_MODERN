DIALOGS = [
[anyone|plyr, "gm_mission_told_bc", [],
 "I will bring the prisoners in alive. Make the cells ready, because this will not be clean work.", "close_window",
   [
       (quest_get_slot, ":quest_target_troop", "qst_bc_capture_prisoners", slot_quest_target_troop),
       (quest_get_slot, ":quest_target_amount", "qst_bc_capture_prisoners", slot_quest_target_amount),
       (assign, reg1, ":quest_target_amount"),
       (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
       (str_store_troop_name_by_count, s3, ":quest_target_troop", ":quest_target_amount"),
       (setup_quest_text, "$random_quest_no"),
       (str_store_string, s2, "@{s9} has requested you to bring him {reg1} {s3} as prisoners."),
   	   (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
  (finish_mission),
   ]],
]
