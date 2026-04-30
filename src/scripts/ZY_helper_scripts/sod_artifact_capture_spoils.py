# COST: medium
SCRIPTS = [
("sod_artifact_capture_spoils",
 [
   (store_script_param_1, ":captor"),
   (store_script_param_2, ":loser"),
   (assign, reg0, 0),

   (try_begin),
     (this_or_next|eq, ":captor", "trp_player"),
     (is_between, ":captor", kingdom_heroes_begin, kingdom_heroes_end),
     (this_or_next|eq, ":loser", "trp_player"),
     (is_between, ":loser", kingdom_heroes_begin, kingdom_heroes_end),
     (neq, ":captor", ":loser"),

     (call_script, "script_sod_artifact_find_best_carried_artifact", ":loser"),
     (eq, reg0, 1),
     (assign, ":source_slot", reg1),
     (assign, ":item_no", reg2),
     (assign, ":item_modifier", reg3),

     (call_script, "script_sod_artifact_can_lord_take_item", ":captor", ":item_no", ":item_modifier"),
     (eq, reg0, 1),
     (assign, ":target_slot", reg1),

     (call_script, "script_sod_artifact_transfer_between_troops", ":loser", ":captor", ":source_slot", ":target_slot", ":item_no", ":item_modifier"),
     (assign, reg0, 1),
   (try_end),
 ]),
]
