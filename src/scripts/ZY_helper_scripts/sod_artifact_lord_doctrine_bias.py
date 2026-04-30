# COST: O(troop inventory)
SCRIPTS = [
("sod_artifact_lord_doctrine_bias",
 [
   (store_script_param_1, ":lord_troop"),
   (assign, ":bias", 0),
   (try_begin),
     (is_between, ":lord_troop", kingdom_heroes_begin, kingdom_heroes_end),
     (call_script, "script_sod_artifact_find_best_carried_artifact", ":lord_troop"),
     (eq, reg0, 1),
     (assign, ":bias", 1),
   (try_end),
   (assign, reg0, ":bias"),
 ]),
]
