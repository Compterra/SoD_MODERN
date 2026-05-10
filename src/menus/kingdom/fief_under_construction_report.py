MENUS = [
("fief_under_construction_report", mnf_enable_hot_keys,
   "Current Construction Report:^^{s2}",
   "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),

      (call_script, "script_get_number_of_hero_centers", "trp_player"),
      (assign, ":no_centers", reg0),

      (assign, ":num_in_report", 0),
      (try_for_range, ":i_center", 0, ":no_centers"),

        # location
        (call_script, "script_troop_get_leaded_center_with_index", "trp_player", ":i_center"),
        (assign, ":cur_center", reg0),

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
            (str_store_string, s2, s1),
          (else_try),
            (str_store_string, s2, "@{s2}^^{s1}"),
          (try_end),
        (try_end),
      (try_end),

      # store the final report
      (try_begin),
        (eq, ":num_in_report", 0),
        (str_store_string, s2, "@No construction projects are currently happening in any of your fiefs."),
      (try_end),
    ],
    [
      ("continue", [], "Continue...", [(jump_to_menu, "mnu_fief_reports")]),
    ]
  ),
]
