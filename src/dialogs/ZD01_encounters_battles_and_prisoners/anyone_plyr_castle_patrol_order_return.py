DIALOGS = [
[anyone|plyr, "castle_patrol_talk", [
    (call_script, "script_sod_player_can_command_castle_patrol", "$g_encountered_party"),
    (eq, reg0, 1),
], "Return to your castle. Put your prisoners, sightings, and road writs before the watch captain.", "close_window", [
    (party_get_slot, ":origin", "$g_encountered_party", slot_party_sod_patrol_origin_castle),
    (party_set_slot, "$g_encountered_party", slot_party_sod_patrol_status, sod_castle_patrol_status_returning),
    (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, "$g_encountered_party", ":origin"),
    (assign, "$g_leave_encounter", 1),
]],
]
