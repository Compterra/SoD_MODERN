MENUS = [
("prisoner_economy_report", mnf_enable_hot_keys,
   "{s9}",
   "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),

      (assign, ":first", 1),
      (assign, ":center_count", 0),
      (call_script, "script_get_number_of_hero_centers", "trp_player"),
      (assign, ":no_centers", reg0),
      (try_for_range, ":i_center", 0, ":no_centers"),
        (call_script, "script_troop_get_leaded_center_with_index", "trp_player", ":i_center"),
        (assign, ":cur_center", reg0),
        (val_add, ":center_count", 1),
        (call_script, "script_sod_center_prisoner_report_to_s20", ":cur_center"),
        (try_begin),
          (eq, ":first", 1),
          (str_store_string, s9, "@{s20}"),
          (assign, ":first", 0),
        (else_try),
          (str_store_string, s9, "@{s9}^^{s20}"),
        (try_end),
      (try_end),

      (try_begin),
        (eq, ":center_count", 0),
        (str_store_string, s9, "@You do not personally hold any centers."),
      (try_end),
      (str_store_string, s9, "@Prisoner Economy Report:^^Non-hero captives now move through prisoner pools, guarded trains, ransom and exchange pressure, forced labor, trials, and liberation outcomes. Prison Towers raise safe capacity and reduce escape pressure; overcrowded holdings can create unrest and make prisoner logistics worth managing.^^{s9}"),
    ],
    [
      ("continue", [], "Continue...", [(jump_to_menu, "mnu_fief_reports")]),
    ]
  ),
]
