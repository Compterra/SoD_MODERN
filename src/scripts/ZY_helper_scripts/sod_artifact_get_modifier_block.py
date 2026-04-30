# COST: trivial
SCRIPTS = [
("sod_artifact_get_modifier_block",
 [
   (store_script_param_1, ":item_modifier"),
   (assign, reg0, 0),
   (try_begin),
     (gt, ":item_modifier", 0),
     (assign, reg0, ":item_modifier"),
     (val_mod, reg0, artifact_modifier_blocks),
   (try_end),
 ]),
]
