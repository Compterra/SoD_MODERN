DIALOGS = [
[anyone, "village_elder_public_health",
  [
    (call_script, "script_sod_center_public_health_brief_to_s0", "$current_town"),
    (str_store_string_reg, s12, s0),
    (call_script, "script_sod_center_public_health_recommendation_to_s0", "$current_town"),
    (str_store_string_reg, s13, s0),
  ],
   "{s12} If you mean to help us, then this is the plain need: {s13}", "village_elder_talk", []],
]
