SIMPLE_TRIGGERS = [
(24,
  [
    # don't allow a random event to occur when the player is a prisoner
    (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 0),

    (call_script, "script_sod_troop_find_faith_candidate"),
    (eq, reg0, 1),
    (assign, "$g_sod_last_noble", reg1),
    (assign, "$g_sod_zealot", reg3),

    # ultimate troops (zealots) locked behind faith: need minimum effective faith for event to fire
    (assign, ":faith", "$g_sod_global_faith"),
    (store_mul, ":holy", "$g_sod_holy", 10),
    (val_sub, ":faith", ":holy"),
    (ge, ":faith", sod_zealot_min_faith),

    # determine if a zealot has come to be
    (store_random_in_range, ":rand", 0, 100),
    (try_begin),
      (ge, ":faith", 500),
      (val_add, ":rand", 50),
    (else_try),
      (ge, ":faith", 400),
      (val_add, ":rand", 32),
    (else_try),
      (ge, ":faith", 300),
      (val_add, ":rand", 16),
    (else_try),
      (ge, ":faith", 200),
      (val_add, ":rand", 8),
    (else_try),
      (ge, ":faith", 100),
      (val_add, ":rand", 4),
    (else_try),
      (ge, ":faith", 50),
      (val_add, ":rand", 2),
    (try_end),
	#SoD Law
	(assign, ":result", 50),
	(val_sub, ":result", "$g_sod_holy_law_modifier"),
    # upgrade the zelaot
    (gt, ":rand", ":result"),
    (jump_to_menu, "mnu_event_holy"),
  ]),
]
