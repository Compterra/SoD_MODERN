DIALOGS = [
[anyone|plyr, "tavern_traveler_lost_companion_thanks", [
    (troop_get_type, reg3, "$last_lost_companion"),
    (try_begin),
      (eq, reg3, 1),
      (str_store_string, s68, "@she"),
      (str_store_string, s69, "@her"),
    (else_try),
      (str_store_string, s68, "@he"),
      (str_store_string, s69, "@him"),
    (try_end),
  ], "Then that is where I ride. If {s68} is there, I will find {s69}.", "tavern_traveler_pretalk", []],
]
