DIALOGS = [
[anyone, "castle_patrol_authority", [
    (call_script, "script_sod_store_castle_patrol_authority_to_s12", "$g_encountered_party"),
    (eq, reg0, 1),
], "{s12}", "castle_patrol_talk", []],
]
