DIALOGS = [
[party_tpl|pt_bandits|auto_proceed, "start", [(eq, "$talk_context", tc_party_encounter)], "Warning: This line should never be displayed.", "looters_1", [
  (call_script, "script_sod_store_hostile_greeting"),
  (str_store_string, s4, "@{s5}"),
  (play_sound, "snd_encounter_looters")
  ]],
]
