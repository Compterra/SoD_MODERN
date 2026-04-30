SIMPLE_TRIGGERS = [
(13,
  [
    # can't be a prisoner
    (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 0),

    # must be a king
    (eq, "$g_sod_king", 1),

    # 1% chance for a randome event to occur
    (store_random_in_range, ":rand" , 0, 200),
    (lt, ":rand", 2),

    # do one of the following events...
    (store_random_in_range, ":rand", 0, 120),
    (try_begin),
      (gt, ":rand", 115), #twan456 I think it's fixed
      (jump_to_menu, "mnu_event_03"),
    (else_try),
      (gt, ":rand", 90),
      (jump_to_menu, "mnu_event_05"),
    (else_try),
      (gt, ":rand", 40),
      (jump_to_menu, "mnu_event_07"),
    (else_try),
      (jump_to_menu, "mnu_event_11"),
    (try_end),
  ]),
]
