DIALOGS = [
[anyone|plyr, "lord_mission_lend_companion_told",
   [(quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop), (call_script, "script_store_troop_name", s3, ":quest_target_troop"), ],
   "Then I will leave {s3} with you for one week.", "lord_tell_mission_lend_companion_accepted", []],
]
