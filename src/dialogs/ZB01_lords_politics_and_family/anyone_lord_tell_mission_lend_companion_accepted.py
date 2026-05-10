DIALOGS = [
[anyone, "lord_tell_mission_lend_companion_accepted", [],
   "I cannot thank you enough, {playername}. Worry not, your companion shall be returned to you with due haste.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
    (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
    (party_remove_members, "p_main_party", ":quest_target_troop", 1),
    (call_script, "script_sod_companion_cleanup_departed_companion", ":quest_target_troop"),
    (assign, "$g_leave_encounter", 1),
   ]],
]
