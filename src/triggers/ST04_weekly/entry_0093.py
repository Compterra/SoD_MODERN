SIMPLE_TRIGGERS = [
(24 * 7,
  [
    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 0),
    (else_try),
      # get the players noble chapter building name
      (store_add, reg0, "str_sod_chapter_0", "$g_sod_country"),
      (str_store_string, s9, reg0),
    (try_end),

    (assign, ":count", 0),
    (try_for_range, ":center_no", centers_begin, centers_end),

      # ensure that this center is currently owned by the player's faction
      (store_faction_of_party, ":center_faction", ":center_no"),
      (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
      (eq, ":center_faction", "fac_player_faction"),

      # ensure that this center has a chapter
      (party_slot_eq, ":center_no", slot_center_has_chapter, 1),

      # Chapters should also provide a little civic order and charitable stability.
      (party_get_slot, ":center_health", ":center_no", slot_center_sod_local_health),
      (party_get_slot, ":center_prosperity", ":center_no", slot_town_prosperity),
      (try_begin),
        (lt, ":center_health", 62),
        (call_script, "script_change_center_health", ":center_no", 1),
      (try_end),
      (try_begin),
        (ge, ":center_health", 55),
        (lt, ":center_prosperity", 68),
        (store_random_in_range, ":chapter_stability_roll", 0, 100),
        (lt, ":chapter_stability_roll", 30),
        (call_script, "script_change_center_prosperity", ":center_no", 1),
      (try_end),

      # remaining effects apply to player only
      (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),

      # keep track of count
      (val_add, ":count", 1),

      # inform the player that their improvements are improving things (if this is part of the player's fief)
      (try_begin),
        (eq, "$g_sod_hide_messages", 0),
        (str_store_party_name_link, s1, ":center_no"),
        (display_message, "@The {s9} in {s1} spreads your name far beyond its walls, adding to your renown while bringing steadier order to the settlement.", renown_color),
      (try_end),
    (try_end),

      # inform the player that their improvements are improving things (if this is part of the player's fief)
      (try_begin),
        (eq, "$g_sod_hide_messages", -1),
        (ge, ":count", 1),
        (display_message, "@Your {s9}s spread your fame throughout the land and bring steadier order to your settlements.", renown_color),
      (try_end),

    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 1),
    (try_end),
  ]),
]
