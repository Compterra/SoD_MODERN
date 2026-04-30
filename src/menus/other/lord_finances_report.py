MENUS = [
("lord_finances_report", mnf_enable_hot_keys,
    "{s1}",
    "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),

      #(str_store_string, s1, "@^You have no lords in your kingdom, as yet!  Speak with your Marshal at one of your towns or castles to correct this!"),
      (str_clear, s1),
      (assign, ":count", 0),
      (try_for_range, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
        (store_troop_faction, ":faction", ":lord"),
        (try_begin),
          (eq, ":faction", "$players_kingdom"), #player's kingdom
          (call_script, "script_store_troop_name", s3, ":lord"),
          (troop_get_slot, reg1, ":lord", slot_troop_wealth),
          (str_store_string, s2, "@{s3} has {reg1} denars."),
          (try_begin),
            (eq, ":count", 0),
            (str_store_string, s1, s2),
          (else_try),
            (str_store_string, s1, "@{s1}^{s2}"),
          (try_end),
          (val_add, ":count", 1),
        (try_end),
      (try_end),
      (str_store_faction_name, s2, "$players_kingdom"),
      (str_store_string, s1, "@The wealth of the lords of {s2}:^^{s1}"),
    ],
    [("continue", [], "Continue...", [(jump_to_menu, "mnu_lord_reports")])]
  ),
]
