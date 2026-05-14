DIALOGS = [
[anyone|plyr, "castle_patrol_talk", [
    (call_script, "script_sod_player_can_command_castle_patrol", "$g_encountered_party"),
    (eq, reg0, 1),
    (call_script, "script_sod_find_castle_patrol_threat_target", "$g_encountered_party"),
    (gt, reg0, 0),
], "Turn on the nearby threat. Let the road see the law arrive with teeth.", "close_window", [
    (call_script, "script_sod_find_castle_patrol_threat_target", "$g_encountered_party"),
    (assign, ":target", reg0),
    (party_set_slot, "$g_encountered_party", slot_party_sod_support_target, ":target"),
    (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_attack_party),
    (party_set_ai_object, "$g_encountered_party", ":target"),
    (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_castle_patrol_scout_report, 1),
    (assign, "$g_leave_encounter", 1),
]],
]
