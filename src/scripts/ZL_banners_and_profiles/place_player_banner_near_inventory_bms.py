SCRIPTS = [
("place_player_banner_near_inventory_bms",
    [
     (troop_get_slot, ":troop_banner_object", "trp_player", slot_troop_banner_scene_prop),
     (try_begin),#normal_banner_begin
       (gt, ":troop_banner_object", 0),
       (replace_scene_props, banner_scene_props_begin, ":troop_banner_object"),
     (else_try),#custom_banner_begin
       (eq, ":troop_banner_object", -1),
       (troop_get_slot, ":flag_spr", "trp_player", slot_troop_custom_banner_flag_type),
       (val_max, ":flag_spr", 0),
       (val_add, ":flag_spr", custom_banner_flag_scene_props_begin),
       (replace_scene_props, banner_scene_props_begin, ":flag_spr"),
     (try_end),
     ]),
]
