# COST: trivial
SCRIPTS = [
("sod_threat_board_calculate_reward",
 [
   (store_script_param_1, ":archetype"),

   (call_script, "script_sod_threat_board_get_archetype", ":archetype"),
    (assign, ":threat_type", reg(0)),
    (assign, ":tier", reg(1)),
    (assign, ":deadline_days", reg(3)),

   (store_mul, ":reward_gold", ":tier", 450),
   (val_add, ":reward_gold", 300),
   (store_character_level, ":level", "trp_player"),
   (store_mul, ":level_bonus", ":level", 20),
   (val_add, ":reward_gold", ":level_bonus"),

   (store_mul, ":reward_xp", ":tier", 250),
   (val_add, ":reward_xp", 150),

   # Shorter notices are riskier: pay a visible urgency premium.
   (store_sub, ":urgency", 12, ":deadline_days"),
   (val_max, ":urgency", 0),
   (store_mul, ":urgency_gold", ":urgency", ":tier"),
   (val_mul, ":urgency_gold", 35),
   (val_add, ":reward_gold", ":urgency_gold"),
   (store_mul, ":urgency_xp", ":urgency", ":tier"),
   (val_mul, ":urgency_xp", 15),
   (val_add, ":reward_xp", ":urgency_xp"),

   (try_begin),
     (eq, ":threat_type", sod_threat_type_relic_thieves),
     (val_add, ":reward_gold", 200),
     (val_add, ":reward_xp", 75),
   (else_try),
     (eq, ":threat_type", sod_threat_type_rogue_company),
     (val_add, ":reward_gold", 175),
     (val_add, ":reward_xp", 60),
   (else_try),
     (eq, ":threat_type", sod_threat_type_faction_problem),
     (val_add, ":reward_gold", 250),
     (val_add, ":reward_xp", 100),
   (else_try),
     (eq, ":threat_type", sod_threat_type_cattle_raiders),
     (val_add, ":reward_gold", 100),
     (val_add, ":reward_xp", 40),
   (try_end),

    (assign, reg(0), ":reward_gold"),
    (assign, reg(1), ":reward_xp"),
    (assign, reg(2), ":urgency_gold"),
    (assign, reg(3), ":urgency_xp"),
 ]),
]
