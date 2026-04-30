SIMPLE_TRIGGERS = [
(10,
  [
    # not a prisoner
    (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 0),

    # is a king
    (eq, "$g_sod_king", 1),

    # honor >= 20
    (ge, "$player_honor", 20),

    # determine the likelihood of this event firing (based on honor)
    (store_random_in_range, ":rand", 0, 200),
    (try_begin),
      (ge, "$player_honor", 100),
      (val_sub, ":rand", 4),
    (else_try),
      (ge, "$player_honor", 70),
      (val_sub, ":rand", 3),
    (else_try),
      (ge, "$player_honor", 50),
      (val_sub, ":rand", 2),
    (else_try),
      (ge, "$player_honor", 30),
      (val_sub, ":rand", 1),
    (try_end),

    # if this event should fire...
    (lt, ":rand", 2),

    # then determine which event it is...
    (store_random_in_range, ":rand", 0, 120),
    (try_begin),
      (gt, ":rand", 80),
      (jump_to_menu, "mnu_event_01"),
    (else_try),
      (gt, ":rand", 40),
      (jump_to_menu, "mnu_event_02"),
    (else_try),
      (jump_to_menu, "mnu_event_08"),
    (try_end),

  ]),
]
