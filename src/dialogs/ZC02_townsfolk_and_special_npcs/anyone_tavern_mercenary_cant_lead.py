DIALOGS = [
[anyone, "tavern_mercenary_cant_lead", [
    (try_begin),
      (gt, reg3, 0),
      (str_store_string, s68, "@we will"),
    (else_try),
      (str_store_string, s68, "@I will"),
    (try_end),
  ], "Then {s68} keep drinking where the work can find us. Come back when your purse or your camp has room.", "close_window", []],
]
