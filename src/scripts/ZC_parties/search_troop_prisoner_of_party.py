SCRIPTS = [
("search_troop_prisoner_of_party",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":prisoner_of", -1),
      (try_for_parties, ":party_no"),
        (eq,  ":prisoner_of", -1),
        (this_or_next|eq, ":party_no", "p_main_party"),
        (ge, ":party_no", centers_begin),
        (party_count_prisoners_of_type, ":troop_found", ":party_no", ":troop_no"),
        (gt, ":troop_found", 0),
        (assign, ":prisoner_of", ":party_no"),
      (try_end),
      (assign, reg0, ":prisoner_of"),
  ]),
]
