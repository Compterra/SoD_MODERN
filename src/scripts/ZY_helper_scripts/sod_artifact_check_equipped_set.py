# COST: low
SCRIPTS = [
("sod_artifact_check_equipped_set",
 [
   (store_script_param_1, ":troop_no"),
   (assign, reg0, 0),
   (assign, ":family", artifact_family_none),
   (try_for_range, ":slot", ek_item_0, ek_head + 1),
     (troop_get_inventory_slot, ":item_no", ":troop_no", ":slot"),
     (gt, ":item_no", 0),
     (item_get_slot, ":flags", ":item_no", slot_item_artifact_flags),
     (store_and, ":is_set", ":flags", artifact_flag_set_piece),
     (gt, ":is_set", 0),
     (item_get_slot, ":piece_family", ":item_no", slot_item_artifact_family),
     (try_begin),
       (eq, ":family", artifact_family_none),
       (assign, ":family", ":piece_family"),
     (try_end),
     (eq, ":piece_family", ":family"),
     (val_add, reg0, 1),
   (try_end),
   (assign, reg1, ":family"),
 ]),
]
