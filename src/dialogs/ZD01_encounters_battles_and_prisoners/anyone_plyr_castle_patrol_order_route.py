DIALOGS = [
[anyone|plyr, "castle_patrol_talk", [
    (call_script, "script_sod_player_can_command_castle_patrol", "$g_encountered_party"),
    (eq, reg0, 1),
], "Shift your patrol. I want another road counted before dusk.", "close_window", [
    (party_get_slot, ":origin", "$g_encountered_party", slot_party_sod_patrol_origin_castle),
    (store_faction_of_party, ":faction_no", "$g_encountered_party"),
    (call_script, "script_sod_find_castle_patrol_route_endpoint", ":origin", ":faction_no"),
    (assign, ":target", reg0),
    (party_set_slot, "$g_encountered_party", slot_party_sod_support_target, ":target"),
    (party_set_slot, "$g_encountered_party", slot_party_sod_patrol_route_endpoint, ":target"),
    (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_patrol_party),
    (party_set_ai_object, "$g_encountered_party", ":target"),
    (assign, "$g_leave_encounter", 1),
]],
]
