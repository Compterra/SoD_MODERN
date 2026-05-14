DIALOGS = [
[party_tpl|pt_patrol_party, "start", [
    (party_slot_eq, "$g_encountered_party", slot_party_sod_support_type, sod_support_type_castle_patrol),
    (call_script, "script_sod_store_nonplayer_patrol_first_line_to_s12", "$g_encountered_party"),
    (eq, reg0, 1),
], "{s12}", "castle_patrol_talk", []],
]
