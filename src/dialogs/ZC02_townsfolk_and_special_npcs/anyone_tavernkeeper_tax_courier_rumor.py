DIALOGS = [
[anyone, "tavernkeeper_pretalk", [
    (call_script, "script_sod_store_tax_courier_rumor_to_s12", 1),
    (eq, reg0, 1),
], "{s12}", "tavernkeeper_talk", [
    (store_current_day, "$g_sod_tax_courier_tavern_rumor_seen_day"),
]],
]
