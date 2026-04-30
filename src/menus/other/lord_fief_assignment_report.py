MENUS = [
("lord_fief_assignment_report", mnf_enable_hot_keys,
   "{s9}",
   "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),

      (str_clear, s9),
      (assign, ":total_lords", 0),
      (assign, ":landed_lords", 0),
      (assign, ":assigned_fiefs", 0),
      (try_for_range, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
        # they must be one of ours
        (troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
        (store_troop_faction, ":faction_no", ":lord"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (val_add, ":total_lords", 1),
        # generate a report for this individual
        (try_begin),
          (assign, ":total_prosperity", 0),
          (call_script, "script_get_number_of_hero_centers", ":lord"),
          (assign, ":no_centers", reg0),
          (val_add, ":assigned_fiefs", ":no_centers"),
          (gt, ":no_centers", 0),
          (val_add, ":landed_lords", 1),
          (str_clear, s1),
          (try_for_range, ":i_center", 0, ":no_centers"),

            # name
            (call_script, "script_troop_get_leaded_center_with_index", ":lord", ":i_center"),
            (assign, ":cur_center", reg0),
            (str_store_party_name, s2, ":cur_center"),

            # prosperity
            (party_get_slot, ":prosperity", ":cur_center", slot_town_prosperity),
            (val_add, ":total_prosperity", ":prosperity"),

            # add the prosperity to the string
            (try_begin),
              (neg|party_slot_eq, ":cur_center", slot_party_type, spt_castle),
              (call_script, "script_get_prosperity_text", s3, ":prosperity"),
              (str_store_string, s2, "@{s2} ({s3})"),
            (try_end),

            # concatenate the strings
            (try_begin),
              (eq, ":i_center", 0),
              (str_store_string_reg, s1, s2),
            (else_try),
              (str_store_string, s1, "@{s1}, {s2}"),
            (try_end),
          (try_end),
          (str_store_string, s1, "@{s1}."),
        (else_try),
          (str_store_string, s1, "@none."),
        (try_end),
        (call_script, "script_store_troop_name", s2, ":lord"),
        (str_store_string, s9, "@{s9}^{s2}: {s1}"),
      (try_end),

      # determine the grand total number of fiefs in the player's kingdom
      (call_script, "script_get_number_of_hero_centers", "trp_player"),
      (store_add, ":total_fiefs", reg0, ":assigned_fiefs"),

      # generate a summary preamble
      (assign, reg1, ":assigned_fiefs"),
      (assign, reg2, ":total_fiefs"),
      (assign, reg3, ":landed_lords"),
      (assign, reg4, ":total_lords"),
      (try_begin),
        (eq, ":total_lords", 0),
        (str_store_string, s9, "@You don't have any lords!"),
      (else_try),
        (eq, ":assigned_fiefs", 0),
        (str_store_string, s9, "@You haven't assigned any of your {reg2} fiefs to any of your {reg4} lords!"),
      (else_try),
        (store_sub, reg5, reg4, reg3),
        (str_store_string, s9, "@You have distributed {reg1} out of {reg2} fiefs amongst {reg5?{reg3} of {reg4}:your {reg4}} lords.^{s9}"),
      (try_end),
      (str_store_string, s9, "@Lord Fief Assignment Report:^^{s9}"),
    ],
    [("continue", [], "Continue...", [(jump_to_menu, "mnu_lord_reports")])]
  ),
]
