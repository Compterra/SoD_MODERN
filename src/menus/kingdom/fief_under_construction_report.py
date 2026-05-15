MENUS = [
("fief_under_construction_report", mnf_enable_hot_keys,
   "Current Construction Report:^^{s98}",
   "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),
      (try_begin),
        (le, "$g_sod_construction_report_return_menu", 0),
        (assign, "$g_sod_construction_report_return_menu", "mnu_fief_reports"),
      (try_end),

      (str_clear, s68),
      (str_clear, s69),
      (str_clear, s97),
      (str_clear, s98),
      (str_clear, s99),

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
          (call_script, "script_describe_current_project", s69, ":cur_center"),
          (str_store_party_name, s68, ":cur_center"),
          (str_store_string, s99, "@{s68}: {s69}"),

          # concatenate together
          (try_begin),
            (eq, ":num_in_report", 1),
            (str_store_string_reg, s98, s99),
          (else_try),
            (str_store_string_reg, s97, s98),
            (str_store_string, s98, "@{s97}^^{s99}"),
          (try_end),
        (try_end),
      (try_end),

      # store the final report
      (try_begin),
        (eq, ":no_centers", 0),
        (str_store_string, s98, "@You do not currently control any manageable fiefs for construction."),
      (else_try),
        (eq, ":num_in_report", 0),
        (str_store_string, s98, "@No construction projects are currently underway in any of your fiefs."),
      (try_end),
    ],
    [
      ("continue", [], "Continue...", [(jump_to_menu, "$g_sod_construction_report_return_menu")]),
    ]
  ),
]
