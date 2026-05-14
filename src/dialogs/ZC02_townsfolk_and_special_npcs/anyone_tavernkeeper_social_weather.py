DIALOGS = [
[anyone, "tavernkeeper_pretalk", [
    (is_between, "$current_town", centers_begin, centers_end),
    (call_script, "script_sod_store_tavernkeeper_social_weather_to_s12", "$current_town"),
    (eq, reg0, 1),
], "{s12}", "tavernkeeper_talk", []],
]
