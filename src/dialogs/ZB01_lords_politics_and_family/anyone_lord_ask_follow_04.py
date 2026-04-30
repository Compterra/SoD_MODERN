DIALOGS = [
[anyone, "lord_ask_follow", [],
   "Lead the way, {playername}! Let us bring death and defeat to all our enemies.", "close_window",
   [(party_set_slot, "$g_talk_troop_party", slot_party_commander_party, "p_main_party"),
    (call_script, "script_party_decide_next_ai_state_under_command", "$g_talk_troop_party"),
    (store_current_hours, ":follow_until_time"),
    (store_add, ":follow_period", 30, "$g_talk_troop_relation"),
    (val_div, ":follow_period", 2),
    (val_add, ":follow_until_time", ":follow_period"),
    (party_set_slot, "$g_encountered_party", slot_party_follow_player_until_time, ":follow_until_time"),
    (party_set_slot, "$g_encountered_party", slot_party_following_player, 1),
    (assign, "$g_leave_encounter", 1)]],
]
