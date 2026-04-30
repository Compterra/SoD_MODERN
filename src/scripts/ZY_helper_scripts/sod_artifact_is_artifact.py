# COST: trivial
SCRIPTS = [
("sod_artifact_is_artifact",
 [
   (store_script_param_1, ":item_no"),
   (assign, reg0, 0),
   (try_begin),
     (gt, ":item_no", 0),
     (item_get_slot, ":flags", ":item_no", slot_item_artifact_flags),
     (gt, ":flags", 0),
     (assign, reg0, 1),
   (try_end),
 ]),
]
