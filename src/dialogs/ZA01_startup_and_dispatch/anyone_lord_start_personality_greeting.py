DIALOGS = [
[anyone, "lord_start", [
    (call_script, "script_sod_store_lord_first_line_to_s12", "$g_talk_troop"),
    (eq, reg0, 1),
], "{s12}", "lord_talk", []],
]
