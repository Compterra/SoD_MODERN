# COST: low
SCRIPTS = [
("sod_player_charge_gold",
 [
   (store_script_param_1, ":amount"),
   (val_max, ":amount", 0),
   (store_troop_gold, ":gold", "trp_player"),
   (assign, ":paid", 0),
   (assign, reg1, 0),
   (try_begin),
     (gt, ":amount", 0),
     (ge, ":gold", ":amount"),
     (assign, ":paid", ":amount"),
     (troop_remove_gold, "trp_player", ":paid"),
     (assign, reg1, 1),
   (try_end),
   (assign, reg0, ":paid"),
 ]),
]
