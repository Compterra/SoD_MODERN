MENUS = [
("fief_under_construction_report", mnf_enable_hot_keys,
   "Current Construction Report:^^{s2}",
   "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),
      (try_begin),
        (le, "$g_sod_construction_report_return_menu", 0),
        (assign, "$g_sod_construction_report_return_menu", "mnu_fief_reports"),
      (try_end),

      (str_clear, s1),
      (str_clear, s2),
      (str_clear, s20),

      (assign, ":no_centers", 0),
      (assign, ":num_in_report", 0),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (party_is_active, ":cur_center"),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (this_or_next|party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
        (faction_slot_eq, ":cur_faction", slot_faction_leader, "trp_player"),
        (val_add, ":no_centers", 1),

        # current construction
        (try_begin),

          # only locations with something under construction
          (neg|party_slot_eq, ":cur_center", slot_center_current_improvement, 0),
          (val_add, ":num_in_report", 1),

          # generate the report for this location
          (call_script, "script_describe_current_project", s20, ":cur_center"),
          (str_store_party_name, s1, ":cur_center"),
          (str_store_string, s1, "@{s1}: {s20}"),

          # concatenate together
          (try_begin),
            (eq, ":num_in_report", 1),
            (str_store_string_reg, s2, s1),
          (else_try),
            (str_store_string, s2, "@{s2}^^{s1}"),
          (try_end),
        (try_end),
      (try_end),

      # store the final report
      (try_begin),
        (eq, ":no_centers", 0),
        (str_store_string, s2, "@You do not currently control any manageable fiefs for construction."),
      (else_try),
        (eq, ":num_in_report", 0),
        (str_store_string, s2, "@No construction projects are currently happening in any of your fiefs."),
      (try_end),
    ],
    [
      ("continue", [], "Continue...", [(jump_to_menu, "$g_sod_construction_report_return_menu")]),
    ]
  ),
]
