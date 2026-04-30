DIALOGS = [
[anyone, "gm_tell_mission", [(eq, "$random_quest_no", "qst_bc_capture_prisoners")],
 "Since you are asking, I am always impressed when justice is served.  Capture me {reg1} {s3}.  You need not worry about the fate of these prisoners, I assure you, they will answer for their crimes.", "gm_mission_told_bc",
 # {reg1} is the number of prisoners, {s3} is the troop type
   [
       (quest_get_slot, ":quest_target_troop", "qst_bc_capture_prisoners", slot_quest_target_troop),
       (quest_get_slot, ":quest_target_amount", "qst_bc_capture_prisoners", slot_quest_target_amount),
       (assign, reg1, ":quest_target_amount"),
       (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
       (str_store_troop_name_by_count, s3, ":quest_target_troop", ":quest_target_amount"),
    ]],
]
