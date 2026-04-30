MENUS = [
(
    "center_tax", mnf_scale_picture|mnf_disable_all_keys,
    "You receive the accumulated rents and taxes of your fiefs, amounting to {reg1} denars.",
    "none",
    [
      (set_background_mesh, "mesh_pic_payment"),

      # collect all taxes at once
      (assign, ":total_tax", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
        (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
        (val_add, ":total_tax", ":accumulated_rents"),
        (val_add, ":total_tax", ":accumulated_tariffs"),
        (party_set_slot, ":center_no", slot_center_accumulated_rents, 0),
        (party_set_slot, ":center_no", slot_center_accumulated_tariffs, 0),
      (try_end),
      (assign, reg1, ":total_tax"),
      (call_script, "script_troop_add_gold", "trp_player", ":total_tax"),
    ],
    [
      ("continue", [], "Continue...",
        [
          (try_begin),
            (party_slot_eq, "$current_town", slot_party_type, spt_village),
            (jump_to_menu, "mnu_village"),
          (else_try),
            (jump_to_menu, "mnu_town"),
          (try_end),
        ]
      ),
    ],
  ),
]
