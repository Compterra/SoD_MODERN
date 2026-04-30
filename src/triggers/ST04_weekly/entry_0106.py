SIMPLE_TRIGGERS = [
(24*7,
  [
    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 0),
    (try_end),

    # for each of your Lords, increase their fealty if you've given them a fief, and reduce it if not (and reduce if they're in prison)
    (try_for_range, ":lord", kingdom_heroes_begin, kingdom_heroes_end),

      # must be active / alive
      (troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),

      # must be a member of our kingdom
      (store_troop_faction, ":faction", ":lord"),
      (eq, ":faction", "fac_player_supporters_faction"),

      # and we must be leader of said kingdom
      (faction_slot_eq, ":faction", slot_faction_leader, "trp_player"),

      # start of discontent
      (assign, ":change", 0),
      (try_begin),
        # hero is in prison - make them unhappy with you (sucks being in chains)
        (troop_slot_ge, ":lord", slot_troop_prisoner_of_party, 0),
        (assign, ":change", -2),
      (else_try),
        # give them a positive bonus based on how many and types of fiefs
        (try_for_range, ":center_no", villages_begin, villages_end),
          (party_slot_eq, ":center_no", slot_town_lord, ":lord"),
          (val_add, ":change", 1),
        (try_end),
        (try_for_range, ":center_no", castles_begin, castles_end),
          (party_slot_eq, ":center_no", slot_town_lord, ":lord"),
          (val_add, ":change", 1),
        (try_end),
        (try_for_range, ":center_no", towns_begin, towns_end),
          (party_slot_eq, ":center_no", slot_town_lord, ":lord"),
          (val_add, ":change", 2),
        (try_end),
        (try_begin),
          # lords without any holdings slowly sour even if they are not imprisoned
          (eq, ":change", 0),
          (assign, ":change", -1),
        (try_end),
      (try_end),

      # apply net change
      (call_script, "script_change_player_relation_with_troop", ":lord", ":change"),

    (try_end),

    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 1),
    (try_end),
  ]
),
]
