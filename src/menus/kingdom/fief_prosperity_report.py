MENUS = [
("fief_prosperity_report", mnf_enable_hot_keys,
   "{s9}",
   "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),

      (try_begin),
        (assign, ":total_prosperity", 0),
        (call_script, "script_get_number_of_hero_centers", "trp_player"),
        (assign, ":no_centers", reg0),
        (gt, ":no_centers", 0),
        (assign, ":first", 1),
        (try_for_range, ":i_center", 0, ":no_centers"),

          # id
          (call_script, "script_troop_get_leaded_center_with_index", "trp_player", ":i_center"),
          (assign, ":cur_center", reg0),

          # prosperity
          (party_get_slot, ":prosperity", ":cur_center", slot_town_prosperity),
          (val_add, ":total_prosperity", ":prosperity"),

          # population
          (party_get_slot, ":population", ":cur_center", slot_center_sod_local_population),

          # ideal prosperity
          #(call_script, "script_get_center_ideal_prosperity", ":cur_center"),
          #(assign, ":ideal", reg0),

          # relationship
          #(party_get_slot, ":relationship", ":cur_center", slot_center_player_relation),
          #(call_script, "script_describe_center_relation", s3, ":relationship"),

          # health
          (party_get_slot, ":health", ":cur_center", slot_center_sod_local_health),

          # taxes & rents
          (party_get_slot, ":accumulated_rents", ":cur_center", slot_center_accumulated_rents),
          (party_get_slot, ":accumulated_tariffs", ":cur_center", slot_center_accumulated_tariffs),
          (store_add, ":taxes", ":accumulated_rents", ":accumulated_tariffs"),

          # generate strings
          (str_store_party_name, s1, ":cur_center"),
          (call_script, "script_describe_center_prosperity", s2, ":cur_center"),
          (call_script, "script_describe_center_health", s3, ":health"),
          (try_begin),
            (lt, ":population", 250),
            (str_store_string, s4, "@{s1} has only a thin tax roll."),
          (else_try),
            (lt, ":population", 700),
            (str_store_string, s4, "@{s1} has a modest tax roll."),
          (else_try),
            (str_store_string, s4, "@{s1} has a broad tax roll."),
          (try_end),

          # combine into a single string (s8)
          (assign, ":skip", 0),
          (try_begin),
            (is_between, ":cur_center", villages_begin, villages_end),

            # land quality
            (call_script, "script_describe_land_quality", s6, ":cur_center"),

            # cattle
            (party_get_slot, ":cattle", ":cur_center", slot_village_number_of_cattle),
            (try_begin),
              (le, ":cattle", 0),
              (str_store_string, s7, "@no visible herds"),
            (else_try),
              (lt, ":cattle", 20),
              (str_store_string, s7, "@a small herd"),
            (else_try),
              (lt, ":cattle", 60),
              (str_store_string, s7, "@a useful herd"),
            (else_try),
              (str_store_string, s7, "@large herds"),
            (try_end),

            (str_store_string, s8, "@{s2} Its fields are {s6}. They have {s7}. {s3}{s4}"),

            # accumulated taxes
            (try_begin),
              (eq, "$g_sod_king", 0),
              (gt, ":taxes", 0),
              (assign, reg1, ":taxes"),
              (str_store_string, s8, "@{s8} Accumulated taxes are {reg1}."),
            (try_end),

          (else_try),

            # castles (they really don't have anything by way of prosperity - just owed rent)
            (is_between, ":cur_center", castles_begin, castles_end),
            (try_begin),
              (eq, "$g_sod_king", 0),
              (lt, ":taxes", 0),
              (str_store_string, s8, "@Unpaid rent at {s1} is {reg1}."),
            (else_try),
              (assign, ":skip", 1),
            (try_end),

          (else_try),

            # town
            (is_between, ":cur_center", towns_begin, towns_end),
            (str_store_string, s8, "@{s2} {s3} {s4}"),

            # accumulated taxes
            (try_begin),
              (eq, "$g_sod_king", 0),
              (gt, ":taxes", 0),
              (assign, reg1, ":taxes"),
              (str_store_string, s8, "@{s8} Accumulated taxes are {reg1}."),
            (try_end),

          (try_end),

          # concatenate together
          (try_begin),
            (eq, ":skip", 0),
            (try_begin),
              (eq, ":first", 1),
              (str_store_string, s9, "@{s8}"),
              (assign, ":first", 0),
            (else_try),
              (str_store_string, s9, "@{s9}^^{s8}"),
            (try_end),
          (try_end),

        (try_end),

        # store the final report
        (store_div, ":prosperity", ":total_prosperity", ":no_centers"),
        (call_script, "script_get_prosperity_text", s8, ":prosperity"),
        (assign, reg2, ":no_centers"),
        (store_sub, reg0, reg2, 1),
        (str_store_string, s9, "@Average prosperity for your {reg2} {reg0?fiefs:fief} is: {s8}^^{s9}"),
      (else_try),
        (str_store_string, s9, "@You don't have any fiefs!"),
      (try_end),
      (str_store_string, s9, "@Fief Prosperity Report:^^{s9}"),
    ],
    [
      ("continue", [], "Continue...", [(jump_to_menu, "mnu_fief_reports")]),
    ]
  ),
]
