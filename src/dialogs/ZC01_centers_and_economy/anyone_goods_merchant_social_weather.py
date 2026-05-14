DIALOGS = [
[anyone, "goods_merchant_pretalk", [
    (is_between, "$current_town", centers_begin, centers_end),
    (call_script, "script_sod_store_goods_merchant_social_weather_to_s12", "$current_town"),
    (eq, reg0, 1),
], "{s12}", "goods_merchant_talk", []],
]
