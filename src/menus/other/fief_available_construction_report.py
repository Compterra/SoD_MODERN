MENUS = [
("fief_available_construction_report", 0,
   "Available Construction Report:^^{s2}",
   "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),

      (call_script, "script_get_number_of_hero_centers", "trp_player"),
      (assign, ":no_centers", reg0),

      (store_current_hours, ":now"),
      (assign, ":complete", 0),
      (assign, ":num_in_report", 0),
      (assign, ":soonest_hour", 10000),
      (assign, ":soonest_center", -1),
      (try_for_range, ":i_center", 0, ":no_centers"),

        # get the center ID
        (call_script, "script_troop_get_leaded_center_with_index", "trp_player", ":i_center"),
        (assign, ":cur_center", reg0),

        # determin if this center has more construction to do
        (try_begin),

          # only consider fiefs who don't currently have a project under way, but do have more projects available
          (call_script, "script_center_has_more_construction_opportunities", ":cur_center"),
          (assign, ":remaining", reg0),
          (try_begin),
            # nothing left to build here
            (eq, ":remaining", 0),
            (val_add, ":complete", 1),
          (else_try),
            # are we currently building something?
            (neg|party_slot_eq, ":cur_center", slot_center_current_improvement, 0),
            (party_get_slot, ":finished", ":cur_center", slot_center_improvement_end_hour),
            (try_begin),
              # record if this is the next project to reach compleation
              (lt, ":finished", ":soonest_hour"),
              (assign, ":soonest_hour", ":finished"),
              (assign, ":soonest_center", ":cur_center"),
            (try_end),
          (else_try),
            # this center can build more and isn't building anything right now
            (val_add, ":num_in_report", 1),

            # generate text for this location
            (str_store_party_name, s1, ":cur_center"),
            (assign, reg0, ":remaining"),
            (store_sub, reg1, ":remaining", 1),
            (str_store_string, s1, "@{s1} has {reg1?{reg0} more projects:one more project} available."),

            # concatenate together
            (try_begin),
              (eq, ":num_in_report", 1),
              (str_store_string, s2, s1),
            (else_try),
              (str_store_string, s2, "@{s2}^{s1}"),
            (try_end),
          (try_end),
        (try_end),
      (try_end),

      # generate the summary
      (try_begin),
        (eq, ":complete", ":no_centers"),
        (str_store_string, s2, "@All of your fiefs are completely built up!  There is absolutely nothing left to build."),
      (else_try),
        (eq, ":num_in_report", 0),
        (str_store_string, s2, "@All of your fiefs that can have a project under construction, do."),
      (try_end),

      # append whichever one will be the next to complete (if any)
      (try_begin),
        (neq, ":soonest_center", -1),
        (store_sub, ":eta", ":soonest_hour", ":now"),
        (store_div, reg1, ":eta", 24),
        (store_mod, reg2, ":eta", 24),
        (str_store_party_name, s1, ":soonest_center"),
        (str_store_string, s2, "@{s2}^^{s1} will be the next one to finish, in {reg1?{reg1} days and :}{reg2} hours."),
      (try_end),
    ],
    [
      ("continue", [], "Continue...", [(jump_to_menu, "mnu_fief_reports")]),
    ]
  ),
]
