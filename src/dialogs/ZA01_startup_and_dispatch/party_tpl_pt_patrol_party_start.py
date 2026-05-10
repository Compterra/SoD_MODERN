DIALOGS = [
[party_tpl|pt_patrol_party, "start", [
    (party_slot_eq, "$g_encountered_party", slot_party_sod_support_type, sod_support_type_castle_patrol),
    (call_script, "script_sod_store_castle_patrol_dialog_context", "$g_encountered_party"),
    (party_get_slot, ":role", "$g_encountered_party", slot_party_sod_patrol_role),
    (neq, ":role", sod_castle_patrol_role_border_harasser),
], "Hold. {s1} patrol, {s3}. We are watching {s2}. State your business.", "castle_patrol_talk", []],
[party_tpl|pt_patrol_party, "start", [
    (party_slot_eq, "$g_encountered_party", slot_party_sod_support_type, sod_support_type_castle_patrol),
    (call_script, "script_sod_store_castle_patrol_dialog_context", "$g_encountered_party"),
    (party_get_slot, ":role", "$g_encountered_party", slot_party_sod_patrol_role),
    (eq, ":role", sod_castle_patrol_role_border_harasser),
], "Careful on this road. {s1} sent us to make enemies nervous, not travelers comfortable. Speak quickly.", "castle_patrol_talk", []],
]
