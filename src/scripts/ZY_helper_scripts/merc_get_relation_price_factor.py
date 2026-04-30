# COST: trivial
SCRIPTS = [
("merc_get_relation_price_factor",
 [
   (store_script_param_1, ":guild_faction"),

   (store_relation, ":rel", ":guild_faction", "fac_player_faction"),
   (assign, reg0, 100),
   (try_begin),
     (ge, ":rel", 75),
     (assign, reg0, 86),
   (else_try),
     (ge, ":rel", 50),
     (assign, reg0, 90),
   (else_try),
     (ge, ":rel", 25),
     (assign, reg0, 95),
   (else_try),
     (lt, ":rel", 0),
     (assign, reg0, 108),
   (try_end),
 ]),
]
