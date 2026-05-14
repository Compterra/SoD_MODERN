DIALOGS = [
[anyone, "mayor_friendly_pretalk", [
    (call_script, "script_sod_store_mayor_social_weather_to_s12", "$current_town"),
    (eq, reg0, 1),
], "{s12}", "mayor_talk", []],
[anyone, "mayor_pretalk", [
    (call_script, "script_sod_store_mayor_social_weather_to_s12", "$current_town"),
    (eq, reg0, 1),
], "{s12}", "mayor_talk", []],
]
