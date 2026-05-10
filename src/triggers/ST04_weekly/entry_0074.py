SIMPLE_TRIGGERS = [
(7 * 24,
    [
      (assign, ":manors", 0),
      (assign, ":inns", 0),
      (try_for_range, ":cur_village", villages_begin, villages_end),

        # Inns & Manors only affect the player as fief owner, or the player as the king
        (store_faction_of_party, ":faction", ":cur_village"),
        (this_or_next|eq, ":faction", "fac_player_supporters_faction"),
        (party_slot_eq, ":cur_village", slot_town_lord, "trp_player"),

        (party_get_slot, ":lord", ":cur_village", slot_town_lord),
        (str_store_party_name_link, s3, ":cur_village"),

        # Manors should provide steadier stewardship in the village itself.
        (try_begin),
          (party_slot_eq, ":cur_village", slot_center_has_manor, 1),
          (ge, ":lord", 0), #avoid unassigned issue
          (party_get_slot, ":village_health", ":cur_village", slot_center_sod_local_health),
          (party_get_slot, ":village_prosperity", ":cur_village", slot_town_prosperity),
          (try_begin),
            (lt, ":village_health", 62),
            (call_script, "script_change_center_health", ":cur_village", 1),
          (try_end),
          (try_begin),
            (lt, ":village_prosperity", 68),
            (store_random_in_range, ":manor_stewardship_roll", 0, 100),
            (lt, ":manor_stewardship_roll", 30),
            (call_script, "script_change_center_prosperity", ":cur_village", 1),
          (try_end),

          # only count it if it applies to the player
          (eq, ":lord", "trp_player"),
          (val_add, ":manors", 1),

          # only display a message if they want the greatest detail
          (eq, "$g_sod_hide_messages", 0),
          (display_message, "@Your manor in {s3} stands as a mark of noble rule, adding to your renown each week.", renown_color),
        (try_end),

        # Inns should help keep village trade and daily life moving.
        (try_begin),
          (party_slot_eq, ":cur_village", slot_center_has_inn, 1),
          (val_add, ":inns", 1),

          (party_get_slot, ":village_health", ":cur_village", slot_center_sod_local_health),
          (party_get_slot, ":village_prosperity", ":cur_village", slot_town_prosperity),
          (try_begin),
            (lt, ":village_health", 55),
            (store_random_in_range, ":inn_recovery_roll", 0, 100),
            (lt, ":inn_recovery_roll", 30),
            (call_script, "script_change_center_health", ":cur_village", 1),
          (try_end),
          (try_begin),
            (lt, ":village_prosperity", 64),
            (store_random_in_range, ":inn_trade_roll", 0, 100),
            (lt, ":inn_trade_roll", 35),
            (call_script, "script_change_center_prosperity", ":cur_village", 1),
          (try_end),

          (try_begin),
            (eq, "$g_sod_hide_messages", 0),
            (display_message, "@Travelers and villagers gather at the inn in {s3}, deepening the people's regard for your rule.", dark_green),
          (try_end),
        (try_end),
      (try_end),

      # give the player a summary if that is what they prefer
      (try_begin),
        (eq, "$g_sod_hide_messages", -1),
        (ge, ":manors", 1),
        (display_message, "@Your village manors uphold your standing and add to your renown.", renown_color),
      (try_end),
      (try_begin),
        (eq, "$g_sod_hide_messages", -1),
        (ge, ":inns", 1),
        (display_message, "@Your inns help keep village opinion favorable toward your rule.", dark_green),
      (try_end),
    ]
  ),
]
