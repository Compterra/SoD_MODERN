DIALOGS = [
[trp_sod_chancellor, "chancellor_lord_prelude",
    [
      # include the player
      (assign, ":num_lords", 1),

      # count lords in kingdom
      (try_for_range, ":lord", kingdom_heroes_begin, kingdom_heroes_end),

        (store_troop_faction, ":faction", ":lord"),

        # logic = "troop is a member of our kindom, or he's about to become one" (being one of the reserved and marked as a hero = is about to become one)
        (troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
        (this_or_next|eq, ":faction", "fac_player_supporters_faction"),
        (is_between, ":lord", "trp_reserved_knight_1",  "trp_knight_6_01"),

        (val_add, ":num_lords", 1),
      (try_end),

      # count centers
      (assign, ":num_centers", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
         (store_faction_of_party, ":center_faction", ":center_no"),
         (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),  # castles are a liability, not a source of income
         (eq, ":center_faction", "fac_player_supporters_faction"),
         (val_add, ":num_centers", 1),
      (try_end),

      (store_sub, "$territory", ":num_centers", ":num_lords"),
      (try_begin),
        (ge, "$territory", 1),
        (assign, reg1, "$territory"),
        (store_sub, reg0, "$territory", 1),
        (str_store_string, s1, "@We have enough territory to support {reg0?{reg1}:one} more {reg0?Lords:Lord}.  Yes, I think this is a wise choice, my {Lord/Lady}."),
      (else_try),
        (str_store_string, s1, "@We need more territory to recruit additional Lords."),
      (try_end),

      # note: when recruiting a new lord, we ONLY choose from the reserved lords
      (assign, "$lords", 0),
      (try_for_range, ":lord", "trp_reserved_knight_1",  "trp_knight_6_01"),

        # don't choose one that's already active, or that was killed
        (neg|troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
        (neg|troop_slot_eq, ":lord", slot_troop_occupation, slto_dead),

        # add them to our array of possible lords
        (troop_set_slot, "trp_temp_array_a", "$lords", ":lord"),
        (val_add, "$lords", 1),
      (try_end),
    ],
    "It requires one income producing center per lord, plus an additional one for yourself.^^{s1}", "chancellor_lord_action",
    [
    ]
  ],
]
