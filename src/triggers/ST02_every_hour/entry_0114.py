SIMPLE_TRIGGERS = [
(12,
  [
    # not a prisoner
    (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 0),

    # yes a king
    (eq, "$g_sod_king", 1),

    # determine if an event should fire
    (store_random_in_range, ":rand", 0, 200),
    (lt, ":rand", 4),

    # determine which event should fire...
    (store_random_in_range, ":rand", 0, 120),
    (try_begin),
        (gt, ":rand", 60),
        (jump_to_menu, "mnu_event_06"),
    (else_try),
        (jump_to_menu, "mnu_event_09"),
    (try_end),

  ]),
]
