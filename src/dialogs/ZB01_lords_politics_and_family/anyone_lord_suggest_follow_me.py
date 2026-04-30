DIALOGS = [
[anyone, "lord_suggest_follow_me", [],
   "Aye, I'll follow you.", "lord_pretalk", [(party_set_slot, "$g_talk_troop_party", slot_party_commander_party, "p_main_party"),
                                (call_script, "script_party_decide_next_ai_state_under_command", "$g_talk_troop_party")]],
]
