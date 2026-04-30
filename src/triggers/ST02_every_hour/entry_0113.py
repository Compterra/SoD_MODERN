SIMPLE_TRIGGERS = [
(11,
  [
    # must not be a prisoner
    (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 0),

    # must be a king
    (eq, "$g_sod_king", 1),

    # honor <= -20!!!
    (le, "$player_honor", -20),

    # determine likelihood of event firing
    (store_random_in_range, ":rand", 0, 200),
    (try_begin),
      (le, "$player_honor", -100),
      (val_sub, ":rand", 4),
    (else_try),
      (le, "$player_honor", -70),
      (val_sub, ":rand", 3),
    (else_try),
      (le, "$player_honor", -50),
      (val_sub, ":rand", 2),
    (else_try),
      (le, "$player_honor", -30),
      (val_sub, ":rand", 1),
    (try_end),
    (lt, ":rand", 2),

    # choose an event to fire... (currently there is only one...)
    (store_random_in_range, ":rand", 0, 120),
    (try_begin),
      (jump_to_menu, "mnu_event_10"),
    (try_end),

  ]),
]
