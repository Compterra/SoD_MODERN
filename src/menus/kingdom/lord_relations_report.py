MENUS = [
("lord_relations_report", 0,
    "{s1}",
    "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),

      (str_clear, s1),
      (try_for_range, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
        (store_troop_faction, ":faction", ":lord"),
        (try_begin),
          (eq, ":faction", "$players_kingdom"), #player's kingdom
          (call_script, "script_store_troop_name", s2, ":lord"),
          #(troop_get_slot, ":relation", ":lord", slot_troop_player_relation),
          (call_script, "script_troop_get_player_relation", ":lord"), # display the effective relation (not the raw value)
          (assign, ":relation", reg0),
          (call_script, "script_get_realtion_name_s3", ":relation"),
          (str_store_string, s1, "@{s1}^{s2} is {s3}"),
        (try_end),
      (try_end),
      (try_begin),
        (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
        (str_store_string, s1, "@Relations with your lords:^{s1}"),
      (else_try),
        (str_store_faction_name, s2, "$players_kingdom"),
        (str_store_string, s1, "@Relations with the lords of the {s2}:^{s1}"),
      (try_end),
    ],
    [("continue", [], "Continue...", [(jump_to_menu, "mnu_lord_reports")])]
  ),
]
