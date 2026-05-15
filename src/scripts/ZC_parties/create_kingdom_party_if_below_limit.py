SCRIPTS = [
("create_kingdom_party_if_below_limit",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":party_type"),

      (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", ":party_type"),
      (assign, ":party_count", reg0),

      (assign, ":party_count_limit", 0),
      (try_begin),
        (eq, ":party_type", spt_kingdom_caravan),
        (assign, ":party_count_limit", 5),
      (else_try),
        (eq, ":party_type", spt_prisoner_train),
        (assign, ":party_count_limit", peak_prisoner_trains),
      (try_end),

      (try_begin),
        (eq, "$g_sod_debug", 1),
        (str_store_faction_name_link, s1, ":faction_no"),
        (assign, reg0, ":party_count"),
        (assign, reg1, ":party_count_limit"),
        (try_begin),
          (eq, ":party_type", spt_prisoner_train),
          (str_store_string, s68, "@prisoner trains"),
        (else_try),
          (str_store_string, s68, "@caravans"),
        (try_end),
        (display_message, "@{s1} has {reg0} out of {reg1} {s68}.", debug_color),
      (try_end),

      (assign, reg0, -1),
      (try_begin),
        (lt, ":party_count", ":party_count_limit"),
        (call_script, "script_cf_create_kingdom_party", ":faction_no", ":party_type"),
      (try_end),
  ]),
]
