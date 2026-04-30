DIALOGS = [
[party_tpl|pt_bandits|auto_proceed, "start", [(eq, "$talk_context", tc_party_encounter)], "Warning: This line should never be displayed.", "looters_1", [
  (str_store_string, s11, "@It's your money or your life, {mate/girlie}. No sudden moves or we'll run you through."),
  (str_store_string, s12, "@Lucky for you, you caught me in a good mood. Give us all your coin and I might just let you live."),
  (str_store_string, s13, "@This a robbery, eh? I givin' you one chance to hand over everythin' you got, or me and my mates'll kill you. Understand?"),
  (store_random_in_range, ":random", 0, 100),
  (val_mod, ":random", 3),
  (val_add, ":random", 11),
  (str_store_string_reg, s4, ":random"),
  (play_sound, "snd_encounter_looters")
  ]],
]
