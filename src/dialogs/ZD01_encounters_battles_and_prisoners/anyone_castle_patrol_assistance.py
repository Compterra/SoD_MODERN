DIALOGS = [
[anyone, "castle_patrol_assistance", [
    (call_script, "script_sod_store_castle_patrol_dialog_context", "$g_encountered_party"),
    (party_get_num_companions, reg10, "$g_encountered_party"),
    (party_get_num_prisoners, reg11, "$g_encountered_party"),
], "We stand at {reg10} fit fighters and carry {reg11} prisoners. {s6}", "castle_patrol_talk", []],
]
