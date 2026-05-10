# COST: medium
SCRIPTS = [
("sod_artifact_init_registry",
 [
   (try_for_range, ":item_no", "itm_blacksmith_adenian_armor", "itm_items_end"),
     (item_set_slot, ":item_no", slot_item_artifact_flags, 0),
   (try_end),

   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_antarian_armor", artifact_family_antarian, artifact_piece_body, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_antarian_boots", artifact_family_antarian, artifact_piece_boots, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_antarian_crown", artifact_family_antarian, artifact_piece_helm, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_antarian_gauntlets", artifact_family_antarian, artifact_piece_gloves, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_antarian_sword", artifact_family_antarian, artifact_piece_weapon, artifact_flag_royal|artifact_flag_set_piece|artifact_flag_weapon, 3),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_antarian_angon", artifact_family_antarian, artifact_piece_ammo, artifact_flag_royal|artifact_flag_set_piece|artifact_flag_weapon, 3),

   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_marinian_armor", artifact_family_marinian, artifact_piece_body, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_marinian_boots", artifact_family_marinian, artifact_piece_boots, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_marinian_crown", artifact_family_marinian, artifact_piece_helm, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_marinian_bolt", artifact_family_marinian, artifact_piece_ammo, artifact_flag_royal|artifact_flag_set_piece|artifact_flag_weapon, 3),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_marinian_crossbow", artifact_family_marinian, artifact_piece_weapon, artifact_flag_royal|artifact_flag_set_piece|artifact_flag_weapon, 3),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_marinian_glaive", artifact_family_marinian, artifact_piece_weapon, artifact_flag_royal|artifact_flag_set_piece|artifact_flag_weapon, 3),

   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_adenian_armor", artifact_family_adenian, artifact_piece_body, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_adenian_boots", artifact_family_adenian, artifact_piece_boots, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_adenian_crown", artifact_family_adenian, artifact_piece_helm, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_adenian_horse", artifact_family_adenian, artifact_piece_horse, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_adenian_lance", artifact_family_adenian, artifact_piece_weapon, artifact_flag_royal|artifact_flag_set_piece|artifact_flag_weapon, 3),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_adenian_shield", artifact_family_adenian, artifact_piece_shield, artifact_flag_royal|artifact_flag_set_piece, 2),

   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_villianese_armor", artifact_family_villianese, artifact_piece_body, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_villianese_crown", artifact_family_villianese, artifact_piece_helm, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_villianese_arrow", artifact_family_villianese, artifact_piece_ammo, artifact_flag_royal|artifact_flag_set_piece|artifact_flag_weapon, 3),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_villianese_bow", artifact_family_villianese, artifact_piece_weapon, artifact_flag_royal|artifact_flag_set_piece|artifact_flag_weapon, 3),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_villianese_scimitar", artifact_family_villianese, artifact_piece_weapon, artifact_flag_royal|artifact_flag_set_piece|artifact_flag_weapon, 3),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_villianese_shield", artifact_family_villianese, artifact_piece_shield, artifact_flag_royal|artifact_flag_set_piece, 2),

   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_zerrikanian_armor", artifact_family_zerrikanian, artifact_piece_body, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_zerrikanian_crown", artifact_family_zerrikanian, artifact_piece_helm, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_zerrikanian_jarid", artifact_family_zerrikanian, artifact_piece_ammo, artifact_flag_royal|artifact_flag_set_piece|artifact_flag_weapon, 3),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_zerrikanian_scepter", artifact_family_zerrikanian, artifact_piece_weapon, artifact_flag_royal|artifact_flag_set_piece|artifact_flag_weapon, 3),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_zerrikanian_horse", artifact_family_zerrikanian, artifact_piece_horse, artifact_flag_royal|artifact_flag_set_piece, 2),
   (call_script, "script_sod_artifact_register_item", "itm_blacksmith_zerrikanian_bow", artifact_family_zerrikanian, artifact_piece_weapon, artifact_flag_royal|artifact_flag_set_piece|artifact_flag_weapon, 3),
 ]),

("sod_artifact_register_item",
 [
   (store_script_param_1, ":item_no"),
   (store_script_param_2, ":family"),
   (store_script_param, ":piece", 3),
   (store_script_param, ":flags", 4),
   (store_script_param, ":tier", 5),
   (item_set_slot, ":item_no", slot_item_artifact_flags, ":flags"),
   (item_set_slot, ":item_no", slot_item_artifact_family, ":family"),
   (item_set_slot, ":item_no", slot_item_artifact_set_piece, ":piece"),
   (item_set_slot, ":item_no", slot_item_artifact_tier, ":tier"),
   (item_set_slot, ":item_no", slot_item_artifact_original_owner, "trp_player"),
 ]),
]
