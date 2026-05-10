SIMPLE_TRIGGERS = [
(24 * 7,
  [
    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 0),
    (try_end),

    (assign, ":count", 0),
    (try_for_range, ":center_no", centers_begin, centers_end),

      # ensure it has a guild
      (party_slot_eq, ":center_no", slot_center_has_guild, 1),

      # ensure that this center is currently owned by the player's faction
      (store_faction_of_party, ":center_faction", ":center_no"),
      (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
      (eq, ":center_faction", "fac_player_faction"),

      # Guilds should also improve circulation of staples and basic urban conditions.
      (party_get_slot, ":center_health", ":center_no", slot_center_sod_local_health),
      (party_get_slot, ":center_prosperity", ":center_no", slot_town_prosperity),
      (party_get_slot, ":food_store", ":center_no", slot_party_food_store),
      (call_script, "script_center_get_food_store_limit", ":center_no"),
      (assign, ":food_store_limit", reg0),
      (try_begin),
        (lt, ":center_health", 65),
        (call_script, "script_change_center_health", ":center_no", 1),
      (try_end),
      (try_begin),
        (gt, ":food_store_limit", 0),
        (store_div, ":guild_food_boost", ":food_store_limit", 24),
        (val_clamp, ":guild_food_boost", 10, 41),
        (store_sub, ":low_stock_threshold", ":food_store_limit", ":guild_food_boost"),
        (val_div, ":low_stock_threshold", 2),
        (store_mul, ":comfortable_stock_threshold", ":food_store_limit", 3),
        (val_div, ":comfortable_stock_threshold", 5),
        (try_begin),
          (lt, ":food_store", ":low_stock_threshold"),
          (val_add, ":food_store", ":guild_food_boost"),
          (val_min, ":food_store", ":food_store_limit"),
          (party_set_slot, ":center_no", slot_party_food_store, ":food_store"),
        (else_try),
          (ge, ":food_store", ":comfortable_stock_threshold"),
          (ge, ":center_health", 60),
          (lt, ":center_prosperity", 82),
          (store_random_in_range, ":guild_trade_surge_roll", 0, 100),
          (lt, ":guild_trade_surge_roll", 30),
          (call_script, "script_change_center_prosperity", ":center_no", 1),
        (try_end),
      (try_end),

      # inform the player that their guild has an effect (all effects are global, so show message always)
      (try_begin),
        (eq, "$g_sod_hide_messages", 0),
        (str_store_party_name_link, s1, ":center_no"),
        (display_message, "@Merchants in {s1} prosper under your guild's protection, drawing fresh commerce and new wealth into the town.", money_color),
      (try_end),

      # remaining effects apply to player only
      (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),

      # keep track of count
      (val_add, ":count", 1),
    (try_end),

      # inform the player that their trade guilds are paying off
      (try_begin),
        (eq, "$g_sod_hide_messages", -1),
        (ge, ":count", 1),
        (display_message, "@Your trade guilds keep commerce lively throughout your realm and strengthen the flow of wealth.", money_color),
      (try_end),

    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 1),
    (try_end),
  ]),
]
