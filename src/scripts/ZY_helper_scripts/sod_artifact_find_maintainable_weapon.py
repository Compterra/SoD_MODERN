# COST: trivial
SCRIPTS = [
("sod_artifact_find_maintainable_weapon",
 [
   (store_script_param_1, ":troop_no"),
   (assign, reg0, 0),  # found
   (assign, reg1, -1), # equipment slot
   (assign, reg2, -1), # item
   (assign, reg3, 0),  # modifier
   (assign, reg4, 0),  # recorded kills
   (assign, reg5, 25), # next milestone threshold
   (assign, ":best_score", -1),

   (try_for_range, ":slot", ek_item_0, ek_item_3 + 1),
     (troop_get_inventory_slot, ":item_no", ":troop_no", ":slot"),
     (gt, ":item_no", 0),
     (item_get_slot, ":flags", ":item_no", slot_item_artifact_flags),
     (store_and, ":is_weapon", ":flags", artifact_flag_weapon),
     (gt, ":is_weapon", 0),
     (item_get_slot, ":tech", ":item_no", slot_item_artifact_technique_flags),
     (store_and, ":already_maintained", ":tech", artifact_tech_reinforced_haft),
     (eq, ":already_maintained", 0),
     (troop_get_inventory_slot_modifier, ":imod", ":troop_no", ":slot"),
     (item_get_slot, ":rank", ":item_no", slot_item_artifact_provenance_rank),
     (item_get_slot, ":tier", ":item_no", slot_item_artifact_tier),
     (call_script, "script_sod_artifact_get_progress", ":item_no", ":imod"),
     (assign, ":kills", reg0),
     (assign, ":next_mark", reg2),
     (store_mul, ":score", ":rank", 100000),
     (store_mul, ":tier_score", ":tier", 10000),
     (val_add, ":score", ":tier_score"),
     (val_add, ":score", ":kills"),
     (try_begin),
       (gt, ":score", ":best_score"),
       (assign, ":best_score", ":score"),
       (assign, reg0, 1),
       (assign, reg1, ":slot"),
       (assign, reg2, ":item_no"),
       (assign, reg3, ":imod"),
       (assign, reg4, ":kills"),
       (assign, reg5, ":next_mark"),
     (try_end),
   (try_end),
 ]),
]
