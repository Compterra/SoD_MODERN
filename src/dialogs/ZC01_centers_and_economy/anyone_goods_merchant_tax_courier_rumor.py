DIALOGS = [
[anyone, "goods_merchant_pretalk", [
    (call_script, "script_sod_store_tax_courier_rumor_to_s12", 3),
    (eq, reg0, 1),
], "{s12}", "goods_merchant_talk", [
    (store_current_day, "$g_sod_tax_courier_merchant_rumor_seen_day"),
]],
]
