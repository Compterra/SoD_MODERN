SIMPLE_TRIGGERS = [
(8,
  [
    # not a prisoner
    (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 0),

    # yes a king
    (eq, "$g_sod_king", 1),

    # determine if an event should fire
    (store_random_in_range, ":rand", 0, 200),
    (try_begin),
      (lt, "$g_sod_global_health", 0),
      (val_add, ":rand", "$g_sod_global_health"),
    (try_end),
    (le, ":rand", 1),

    # choose which event fires
    (store_random_in_range, ":rand", 0, 120),
    (try_begin),
      (gt, ":rand", 75),
      (jump_to_menu, "mnu_event_12"),
    (else_try),
      (gt, ":rand", 35),
      (jump_to_menu, "mnu_event_13"),
    (else_try),
      (gt, ":rand", 10),
      (jump_to_menu, "mnu_event_14"),
    (else_try),
      (jump_to_menu, "mnu_event_15"),
    (try_end),
  ]),
]
