SIMPLE_TRIGGERS = [
(24 * 7,
  [
  (assign, ":stop", 0),
	(try_begin),
		(lt, "$g_sod_clergy_happines", -95),
		(assign, ":stop", 1),
		(display_message, "@The clergy have turned against your rule; your temples fall silent until relations with the Temple improve.", dark_red),
	(try_end),
	(eq, ":stop", 0),
    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 0),
    (try_end),

    (assign, ":count", 0),
    (try_for_range, ":center_no", centers_begin, centers_end),

      # never castles - they don't track local faith at all (no tax base, no faith base)
      (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),

      # ensure that this center is currently owned by the player's faction
      (store_faction_of_party, ":center_faction", ":center_no"),
      (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
      (eq, ":center_faction", "fac_player_faction"),

      # and that this center has a temple or chapel (WTF do we need two different slot sets for chapel and temple?)
      (this_or_next|party_slot_eq, ":center_no", slot_center_has_chapel, 1),
      (party_slot_eq, ":center_no", slot_center_has_temple, 1),

      # keep track of count
      (val_add, ":count", 1),

      # improve faith (local & global)
      (party_get_slot, ":faith", ":center_no", slot_center_sod_local_faith),
      (val_add, ":faith", "$g_sod_building_temple_local_faith"),
      (val_clamp, ":faith", -100, 201),
      (party_set_slot, ":center_no", slot_center_sod_local_faith, ":faith"),
      (val_add, "$g_sod_global_faith", "$g_sod_building_temple_global_faith"),
      (val_clamp, "$g_sod_global_faith", -2000, 2001),

      # Temples should also reinforce local cohesion when the center can sustain it.
      (party_get_slot, ":center_health", ":center_no", slot_center_sod_local_health),
      (party_get_slot, ":center_prosperity", ":center_no", slot_town_prosperity),
      (party_get_slot, ":food_store", ":center_no", slot_party_food_store),
      (call_script, "script_center_get_food_store_limit", ":center_no"),
      (assign, ":food_store_limit", reg0),
      (try_begin),
        (lt, ":center_health", 63),
        (call_script, "script_change_center_health", ":center_no", 1),
      (try_end),
      (try_begin),
        (ge, ":faith", 35),
        (lt, ":center_prosperity", 68),
        (store_random_in_range, ":temple_prosperity_roll", 0, 100),
        (lt, ":temple_prosperity_roll", 25),
        (call_script, "script_change_center_prosperity", ":center_no", 1),
      (try_end),
      (try_begin),
        (gt, ":food_store_limit", 0),
        (store_mul, ":temple_stable_supply_threshold", ":food_store_limit", 3),
        (val_div, ":temple_stable_supply_threshold", 5),
        (ge, ":food_store", ":temple_stable_supply_threshold"),
        (ge, ":center_health", 58),
        (ge, ":faith", 45),
        (lt, ":center_prosperity", 78),
        (store_random_in_range, ":temple_cohesion_roll", 0, 100),
        (lt, ":temple_cohesion_roll", 25),
        (call_script, "script_change_center_prosperity", ":center_no", 1),
      (try_end),

      # increase this center's realation with the player
      # Only when the player is the center lord OR the player is the faction leader (king).
      (try_begin),
        (this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (faction_slot_eq, ":center_faction", slot_faction_leader, "trp_player"),
        (party_get_slot, ":cur_relation", ":center_no", slot_center_player_relation),
        (val_add, ":cur_relation", "$g_sod_building_temple_reputation"),
        (val_clamp, ":cur_relation", -100, 101),
        (party_set_slot, ":center_no", slot_center_player_relation, ":cur_relation"),
      (try_end),

      # indicate that the player's temples are increasing faith
      (try_begin),
        (eq, "$g_sod_hide_messages", 0),
        (str_store_party_name_link, s1, ":center_no"),
        (store_add, reg0, "str_sod_temple_improve_0", "$g_sod_faith"),
        (str_store_string, s1, reg0),
        (display_message, s1, faith_color),
      (try_end),
    (try_end),

    # indicate that the player's temples are increasing faith
    (try_begin),
      (eq, "$g_sod_hide_messages", -1),
      (ge, ":count", 1),
      #(str_store_party_name_link, s1, ":center_no"),
      (store_add, reg0, "str_sod_temple_summary_0", "$g_sod_faith"),
      (str_store_string, s1, reg0),
      (display_message, s1, faith_color),
    (try_end),

    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 1),
    (try_end),
  ]),
]
