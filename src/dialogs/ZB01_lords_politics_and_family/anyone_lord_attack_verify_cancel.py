DIALOGS = [
[anyone, "lord_attack_verify_cancel", [], "Be gone, then.", "close_window", [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1), (assign, "$g_leave_encounter", 1)]],
]
