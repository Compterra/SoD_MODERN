SCRIPTS = [
("cf_sod_companion_campaign_available",
    [
      (store_script_param_1, ":companion"),
      (store_script_param_2, ":required_mode"),

      (assign, ":available", 1),

      (try_begin),
        (lt, ":companion", companions_begin),
        (assign, ":available", 0),
      (else_try),
        (ge, ":companion", companions_end),
        (assign, ":available", 0),
      (else_try),
        (neg|troop_slot_eq, ":companion", slot_troop_occupation, slto_player_companion),
        (assign, ":available", 0),
      (else_try),
        (neg|call_script, "script_cf_sod_companion_in_main_party", ":companion"),
        (assign, ":available", 0),
      (try_end),

      (try_begin),
        (eq, ":available", 1),
        (this_or_next|eq, ":required_mode", sod_companion_campaign_mode_scene),
        (eq, ":required_mode", sod_companion_campaign_mode_battle),
        (store_troop_health, ":companion_health", ":companion"),
        (lt, ":companion_health", 20),
        (assign, ":available", 0),
      (try_end),

      (try_begin),
        (eq, ":available", 1),
        (troop_slot_ge, ":companion", slot_troop_companion_personal_quest_stage, sod_companion_quest_resolved_good),
        (assign, ":available", 0),
      (try_end),

      (try_begin),
        (eq, ":available", 1),
        (troop_slot_eq, ":companion", slot_troop_companion_personal_quest_stage, sod_companion_quest_resolved_hard),
        (assign, ":available", 0),
      (try_end),

      (eq, ":available", 1),
  ]),
]
