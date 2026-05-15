MENUS = [
("fief_prosperity_report", mnf_enable_hot_keys,
   "{s98}",
   "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),
      (str_clear, s98),

      (try_begin),
        (assign, ":total_prosperity", 0),
        (assign, ":worst_score", -1),
        (assign, ":worst_center", -1),
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
          (call_script, "script_sod_center_public_health_brief_to_s0", ":cur_center"),
          (str_store_string_reg, s5, s0),

          # taxes & rents
          (party_get_slot, ":accumulated_rents", ":cur_center", slot_center_accumulated_rents),
          (party_get_slot, ":accumulated_tariffs", ":cur_center", slot_center_accumulated_tariffs),
          (store_add, ":taxes", ":accumulated_rents", ":accumulated_tariffs"),

          # Stewardship priority score: health and population matter everywhere;
          # prosperity only applies to towns/villages, while castles mostly show rent strain.
          (assign, ":issue_score", 0),
          (try_begin),
            (lt, ":health", 35),
            (store_sub, ":health_issue", 35, ":health"),
            (val_add, ":issue_score", ":health_issue"),
          (try_end),
          (try_begin),
            (this_or_next|is_between, ":cur_center", towns_begin, towns_end),
            (is_between, ":cur_center", villages_begin, villages_end),
            (lt, ":prosperity", 35),
            (store_sub, ":prosperity_issue", 35, ":prosperity"),
            (val_add, ":issue_score", ":prosperity_issue"),
          (try_end),
          (try_begin),
            (lt, ":population", 250),
            (val_add, ":issue_score", 15),
          (try_end),
          (try_begin),
            (lt, ":taxes", 0),
            (val_add, ":issue_score", 10),
          (try_end),
          (try_begin),
            (gt, ":issue_score", ":worst_score"),
            (assign, ":worst_score", ":issue_score"),
            (assign, ":worst_center", ":cur_center"),
          (try_end),

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

            (str_store_string, s8, "@{s2} Its fields are {s6}. They have {s7}. {s3}{s4} {s5}"),

            # accumulated taxes
            (try_begin),
              (eq, "$g_sod_king", 0),
              (gt, ":taxes", 0),
              (assign, reg1, ":taxes"),
              (str_store_string_reg, s96, s8),
              (str_store_string, s8, "@{s96} Accumulated taxes are {reg1}."),
            (try_end),

          (else_try),

            # castles (they really don't have anything by way of prosperity - just owed rent)
            (is_between, ":cur_center", castles_begin, castles_end),
            (try_begin),
              (eq, "$g_sod_king", 0),
              (lt, ":taxes", 0),
              (assign, reg1, ":taxes"),
              (str_store_string, s8, "@Unpaid rent at {s1} is {reg1}."),
            (else_try),
              (assign, ":skip", 1),
            (try_end),

          (else_try),

            # town
            (is_between, ":cur_center", towns_begin, towns_end),
            (str_store_string, s8, "@{s2} {s3} {s4} {s5}"),

            # accumulated taxes
            (try_begin),
              (eq, "$g_sod_king", 0),
              (gt, ":taxes", 0),
              (assign, reg1, ":taxes"),
              (str_store_string_reg, s96, s8),
              (str_store_string, s8, "@{s96} Accumulated taxes are {reg1}."),
            (try_end),

          (try_end),

          # concatenate together
          (try_begin),
            (eq, ":skip", 0),
            (try_begin),
              (eq, ":first", 1),
              (str_store_string, s98, "@{s8}"),
              (assign, ":first", 0),
            (else_try),
              (str_store_string_reg, s97, s98),
              (str_store_string, s98, "@{s97}^^{s8}"),
            (try_end),
          (try_end),

        (try_end),

        # store the final report
        (store_div, ":prosperity", ":total_prosperity", ":no_centers"),
        (call_script, "script_get_prosperity_text", s8, ":prosperity"),
        (assign, reg2, ":no_centers"),
        (assign, reg3, ":worst_score"),
        (try_begin),
          (eq, reg2, 1),
          (str_store_string, s68, "@fief"),
        (else_try),
          (str_store_string, s68, "@fiefs"),
        (try_end),
        (str_store_string, s70, "@Steward priority: no urgent weakness stands out. Keep food, health, roads, and taxes steady."),
        (try_begin),
          (is_between, ":worst_center", centers_begin, centers_end),
          (gt, ":worst_score", 0),
          (str_store_party_name, s69, ":worst_center"),
          (party_get_slot, ":priority_health", ":worst_center", slot_center_sod_local_health),
          (party_get_slot, ":priority_prosperity", ":worst_center", slot_town_prosperity),
          (party_get_slot, ":priority_population", ":worst_center", slot_center_sod_local_population),
          (party_get_slot, ":priority_rents", ":worst_center", slot_center_accumulated_rents),
          (party_get_slot, ":priority_tariffs", ":worst_center", slot_center_accumulated_tariffs),
          (store_add, ":priority_taxes", ":priority_rents", ":priority_tariffs"),
          (try_begin),
            (lt, ":priority_health", 35),
            (str_store_string, s70, "@Steward priority: {s69}. Health is the immediate weakness; move food, secure recovery, or build support before prosperity slips further."),
          (else_try),
            (this_or_next|is_between, ":worst_center", towns_begin, towns_end),
            (is_between, ":worst_center", villages_begin, villages_end),
            (lt, ":priority_prosperity", 35),
            (str_store_string, s70, "@Steward priority: {s69}. Prosperity is the immediate weakness; secure roads, trade routes, and recovery before the tax base shrinks."),
          (else_try),
            (lt, ":priority_population", 250),
            (str_store_string, s70, "@Steward priority: {s69}. The tax roll is thin; protect people, food, and migration before squeezing revenue."),
          (else_try),
            (lt, ":priority_taxes", 0),
            (str_store_string, s70, "@Steward priority: {s69}. Unpaid rent is the visible problem; settle obligations before garrison strain becomes politics."),
          (else_try),
            (str_store_string, s70, "@Steward priority: {s69}. It is the weakest fief by combined health, prosperity, population, and rent pressure. Priority score {reg3}."),
          (try_end),
        (try_end),
        (str_store_string_reg, s97, s98),
        (str_store_string, s98, "@Average prosperity for your {reg2} {s68} is: {s8}^^{s70}^^{s97}"),
      (else_try),
        (str_store_string, s98, "@You don't have any fiefs!"),
      (try_end),
      (str_store_string_reg, s97, s98),
      (str_store_string, s98, "@Fief Prosperity Report:^^{s97}"),
    ],
    [
      ("continue", [], "Continue...", [(jump_to_menu, "mnu_fief_reports")]),
    ]
  ),
]
