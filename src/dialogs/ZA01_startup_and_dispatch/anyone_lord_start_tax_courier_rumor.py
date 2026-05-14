DIALOGS = [
[anyone, "lord_start", [
    (call_script, "script_sod_store_tax_courier_rumor_to_s12", 2),
    (eq, reg0, 1),
], "{s12}", "lord_start", [
    (store_current_day, "$g_sod_tax_courier_lord_rumor_seen_day"),
]],
]
