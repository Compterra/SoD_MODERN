SIMPLE_TRIGGERS = [
(24 * 7,
  [
    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 0),
    (try_end),

    (assign, ":count", 0),
    (try_for_range, ":center_no", centers_begin, centers_end),

      # ensure that this center is currently owned by the player's faction
      (store_faction_of_party, ":center_faction", ":center_no"),
      (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
      (eq, ":center_faction", "fac_player_faction"),

      # check if this center has a stables
      (party_slot_eq, ":center_no", slot_center_has_stables, 1),

      # Stables should also improve circulation, supply, and day-to-day conditions.
      (party_get_slot, ":center_health", ":center_no", slot_center_sod_local_health),
      (party_get_slot, ":center_prosperity", ":center_no", slot_town_prosperity),
      (party_get_slot, ":food_store", ":center_no", slot_party_food_store),
      (call_script, "script_center_get_food_store_limit", ":center_no"),
      (assign, ":food_store_limit", reg0),
      (try_begin),
        (lt, ":center_prosperity", 65),
        (call_script, "script_change_center_prosperity", ":center_no", 1),
      (else_try),
        (ge, ":center_health", 55),
        (lt, ":center_prosperity", 75),
        (store_random_in_range, ":stable_trade_roll", 0, 100),
        (lt, ":stable_trade_roll", 35),
        (call_script, "script_change_center_prosperity", ":center_no", 1),
      (try_end),
      (try_begin),
        (lt, ":center_health", 58),
        (call_script, "script_change_center_health", ":center_no", 1),
      (try_end),
      (try_begin),
        (gt, ":food_store_limit", 0),
        (store_div, ":stable_food_boost", ":food_store_limit", 28),
        (val_clamp, ":stable_food_boost", 8, 32),
        (store_mul, ":stable_low_stock_threshold", ":food_store_limit", 2),
        (val_div, ":stable_low_stock_threshold", 5),
        (store_mul, ":stable_comfortable_stock_threshold", ":food_store_limit", 3),
        (val_div, ":stable_comfortable_stock_threshold", 5),
        (try_begin),
          (lt, ":food_store", ":stable_low_stock_threshold"),
          (val_add, ":food_store", ":stable_food_boost"),
          (val_min, ":food_store", ":food_store_limit"),
          (party_set_slot, ":center_no", slot_party_food_store, ":food_store"),
        (else_try),
          (ge, ":food_store", ":stable_comfortable_stock_threshold"),
          (ge, ":center_health", 50),
          (lt, ":center_prosperity", 78),
          (store_random_in_range, ":stable_logistics_roll", 0, 100),
          (lt, ":stable_logistics_roll", 25),
          (call_script, "script_change_center_prosperity", ":center_no", 1),
        (try_end),
      (try_end),

      (try_begin),
        # remaining effects apply to player only
        (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),

        # keep track of count
        (val_add, ":count", 1),

        # inform the player that their improvements are improving things
        (try_begin),
          (eq, "$g_sod_hide_messages", 0),
          (str_store_party_name_link, s1, ":center_no"),
          (display_message, "@Well-kept stables in {s1} keep riders, pack animals, and supplies moving, adding to your renown while lending strength to the town's daily life.", renown_color),
        (try_end),
      (try_end),
    (try_end),

      # inform the player that their improvements are improving things
      (try_begin),
        (eq, "$g_sod_hide_messages", -1),
        (ge, ":count", 1),
        (display_message, "@Your stables enhance your reputation across the realm and help keep local supply lines strong.", renown_color),
      (try_end),

    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 1),
    (try_end),
  ]),
]
