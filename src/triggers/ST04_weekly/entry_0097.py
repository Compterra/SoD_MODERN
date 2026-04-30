SIMPLE_TRIGGERS = [
(24 * 7,
  [
    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 0),
    (try_end),

    (assign, ":count", 0),
    (try_for_range, ":center_no", centers_begin, centers_end),

      # only for centers that have a mill
      (party_slot_eq, ":center_no", slot_center_has_mill, 1),

      # increase the prosperity
      (set_show_messages, 0),
      (call_script, "script_change_center_prosperity", ":center_no", "$g_sod_building_mill_prosperity"),
      (set_show_messages, 1),

      # Mills should also support local food processing and baseline living conditions.
      (party_get_slot, ":center_health", ":center_no", slot_center_sod_local_health),
      (party_get_slot, ":center_prosperity", ":center_no", slot_town_prosperity),
      (party_get_slot, ":food_store", ":center_no", slot_party_food_store),
      (call_script, "script_center_get_food_store_limit", ":center_no"),
      (assign, ":food_store_limit", reg0),
      (try_begin),
        (lt, ":center_health", 60),
        (call_script, "script_change_center_health", ":center_no", 1),
      (try_end),
      (try_begin),
        (gt, ":food_store_limit", 0),
        (store_div, ":mill_food_boost", ":food_store_limit", 20),
        (val_clamp, ":mill_food_boost", 12, 55),
        (store_mul, ":mill_low_stock_threshold", ":food_store_limit", 2),
        (val_div, ":mill_low_stock_threshold", 3),
        (store_mul, ":mill_comfortable_stock_threshold", ":food_store_limit", 3),
        (val_div, ":mill_comfortable_stock_threshold", 5),
        (try_begin),
          (lt, ":food_store", ":mill_low_stock_threshold"),
          (val_add, ":food_store", ":mill_food_boost"),
          (val_min, ":food_store", ":food_store_limit"),
          (party_set_slot, ":center_no", slot_party_food_store, ":food_store"),
        (else_try),
          (ge, ":food_store", ":mill_comfortable_stock_threshold"),
          (ge, ":center_health", 55),
          (lt, ":center_prosperity", 75),
          (store_random_in_range, ":mill_processing_roll", 0, 100),
          (lt, ":mill_processing_roll", 30),
          (call_script, "script_change_center_prosperity", ":center_no", 1),
        (try_end),
      (try_end),

      # ensure that this center is currently owned by the player's faction
      (store_faction_of_party, ":center_faction", ":center_no"),
      (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
      (eq, ":center_faction", "fac_player_faction"),

      # improve player's relationship with this village
#      (party_get_slot, ":cur_relation", ":center_no", slot_center_player_relation),
#      (val_add, ":cur_relation", 1),
#      (party_set_slot, ":center_no", slot_center_player_relation, ":cur_relation"),

      # remaining effects apply to player only
      (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),

      # keep track of count
      (val_add, ":count", 1),

      # inform player
      (try_begin),
        (eq, "$g_sod_hide_messages", 0),
        (str_store_party_name_link, s1, ":center_no"),
        (display_message, "@The mills of {s1} keep grain moving and bring steady profit to the village each week.", money_color),
      (try_end),
    (try_end),

    # inform player
    (try_begin),
      (eq, "$g_sod_hide_messages", 0),
      (ge, ":count", 1),
      (display_message, "@Your village mills keep flour, trade, and profit flowing through your lands each week.", money_color),
    (try_end),

    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 1),
    (try_end),
  ]),
]
