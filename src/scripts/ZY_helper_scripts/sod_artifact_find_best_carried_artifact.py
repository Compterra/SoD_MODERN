# COST: medium
SCRIPTS = [
("sod_artifact_find_best_carried_artifact",
 [
   (store_script_param_1, ":troop_no"),
   (assign, reg0, 0),  # found
   (assign, reg1, -1), # inventory/equipment slot
   (assign, reg2, -1), # item
   (assign, reg3, 0),  # modifier
   (assign, ":best_score", -1),

   (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
   (try_for_range, ":slot", 0, ":inv_cap"),
     (troop_get_inventory_slot, ":item_no", ":troop_no", ":slot"),
     (gt, ":item_no", 0),
     (item_get_slot, ":flags", ":item_no", slot_item_artifact_flags),
     (gt, ":flags", 0),
     (troop_get_inventory_slot_modifier, ":imod", ":troop_no", ":slot"),
     (item_get_slot, ":rank", ":item_no", slot_item_artifact_provenance_rank),
     (item_get_slot, ":tier", ":item_no", slot_item_artifact_tier),
     (call_script, "script_sod_artifact_get_progress", ":item_no", ":imod"),
     (assign, ":kills", reg0),
     (store_mul, ":score", ":rank", 100000),
     (store_mul, ":tier_score", ":tier", 10000),
     (val_add, ":score", ":tier_score"),
     (val_add, ":score", ":kills"),
     (try_begin),
       (lt, ":slot", ek_head),
       (val_add, ":score", 500),
     (try_end),
     (try_begin),
       (gt, ":score", ":best_score"),
       (assign, ":best_score", ":score"),
       (assign, reg0, 1),
       (assign, reg1, ":slot"),
       (assign, reg2, ":item_no"),
       (assign, reg3, ":imod"),
     (try_end),
   (try_end),
 ]),
]
