DIALOGS = [
[anyone, "village_elder_pretalk", [
    (call_script, "script_sod_store_village_elder_social_weather_to_s12", "$current_town"),
    (eq, reg0, 1),
], "{s12}", "village_elder_talk", []],
]
