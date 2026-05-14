DIALOGS = [
[trp_sod_marshal|plyr|repeat_for_parties, "marshal_nobles_choose",
    [
      (store_repeat_object, ":center_no"),

      # don't clutter their options with their currently chosen option
      (neq, ":center_no", "$g_sod_nobles_gather_at"),

      # must be in the player's realm
      (store_faction_of_party, ":center_faction", ":center_no"),
      (eq, ":center_faction", "fac_player_supporters_faction"),

      # check if this location has a chapter house
      (party_slot_eq, ":center_no", slot_center_has_chapter, 1),

      (str_store_party_name, s1, ":center_no"),
      (troop_get_slot, ":here", "trp_sod_marshal", slot_troop_sod_court),
      (store_sub, reg0, ":center_no", ":here"),
      (try_begin),
        (neq, reg0, 0),
        (str_store_string, s2, "@at {s1}"),
      (else_try),
        (str_store_string, s2, "@them here"),
      (try_end),
    ],
    "Recruit {s2}.", "marshal_nobles",
    [
      # simply store their new choice
      (store_repeat_object, "$g_sod_nobles_gather_at"),
    ]
  ],
]
