SIMPLE_TRIGGERS = [
(24 * 7,
  [
    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 0),
    (try_end),
	(assign, ":stop", 0),
	(try_begin),
		(lt, "$g_sod_clergy_happines", -95),
		(assign, ":stop", 1),
		(display_message, "@The clergy have turned against you; your holy buildings fall quiet until relations with the Temple improve.", dark_red),
	(try_end),
	(eq, ":stop", 0),
    (assign, ":count", 0),
    (try_for_range, ":center_no", centers_begin, centers_end),

      # never castles - they don't track local faith at all (no tax base, no faith base)
      (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),

      # ensure that this center is currently owned by the player's faction
      (store_faction_of_party, ":center_faction", ":center_no"),
      (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
      (eq, ":center_faction", "fac_player_faction"),

      # and that this village has a shrine
      (party_slot_eq, ":center_no", slot_center_has_shrine, 1),

      # keep track of count
      (val_add, ":count", 1),

      # increase the local & global faithful
      (party_get_slot, ":faith", ":center_no", slot_center_sod_local_faith),
      (val_add, ":faith", "$g_sod_building_shrine_local_faith"),
      (val_clamp, ":faith", -100, 201),
      (party_set_slot, ":center_no", slot_center_sod_local_faith, ":faith"),
      (try_begin),
        (gt, "$g_sod_faith", 0),
        (call_script, "script_sod_change_center_faith_support", ":center_no", "$g_sod_faith", "$g_sod_building_shrine_local_faith"),
        (call_script, "script_sod_get_center_faith_profile", ":center_no"),
        (assign, ":faith", reg2),
      (try_end),
      (val_add, "$g_sod_global_faith", "$g_sod_building_shrine_global_faith"),
      (val_clamp, "$g_sod_global_faith", -2000, 2001),

      # Shrines should also support local morale and day-to-day steadiness.
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
        (ge, ":faith", 30),
        (lt, ":center_prosperity", 68),
        (store_random_in_range, ":shrine_prosperity_roll", 0, 100),
        (lt, ":shrine_prosperity_roll", 25),
        (call_script, "script_change_center_prosperity", ":center_no", 1),
      (try_end),
      (try_begin),
        (gt, ":food_store_limit", 0),
        (store_mul, ":shrine_stable_supply_threshold", ":food_store_limit", 3),
        (val_div, ":shrine_stable_supply_threshold", 5),
        (ge, ":food_store", ":shrine_stable_supply_threshold"),
        (ge, ":center_health", 56),
        (ge, ":faith", 40),
        (lt, ":center_prosperity", 76),
        (store_random_in_range, ":shrine_cohesion_roll", 0, 100),
        (lt, ":shrine_cohesion_roll", 20),
        (call_script, "script_change_center_prosperity", ":center_no", 1),
      (try_end),

      # increase this center's realation with the player
      # Only when the player is the center lord OR the player is the faction leader (king).
      (try_begin),
        (this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (faction_slot_eq, ":center_faction", slot_faction_leader, "trp_player"),
        (party_get_slot, ":cur_relation", ":center_no", slot_center_player_relation),
        (val_add, ":cur_relation", "$g_sod_building_shrine_reputation"),
        (val_clamp, ":cur_relation", -100, 101),
        (party_set_slot, ":center_no", slot_center_player_relation, ":cur_relation"),
      (try_end),

      # let the player know that their efforts are not in vain
      (try_begin),
        (eq, "$g_sod_hide_messages", 0),
        (is_between, "$g_sod_faith", sod_faiths_begin, sod_faiths_end),
        (str_store_party_name_link, s1, ":center_no"),
        (store_add, reg0, "str_sod_shrine_improve_0", "$g_sod_faith"),
        (str_store_string, s1, reg0),
        (display_message, s1, faith_color),
      (try_end),
    (try_end),

    # let the player know that their efforts are not in vain
    (try_begin),
      (eq, "$g_sod_hide_messages", -1),
      (ge, ":count", 1),
      (is_between, "$g_sod_faith", sod_faiths_begin, sod_faiths_end),
      (store_add, reg0, "str_sod_shrine_summary_0", "$g_sod_faith"),
      (str_store_string, s1, reg0),
      (display_message, s1, faith_color),
    (try_end),
	
	#CHAPELS
	(try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 0),
    (try_end),

    (assign, ":count", 0),
    (try_for_range, ":center_no", centers_begin, centers_end),
      # castle
      (party_slot_eq, ":center_no", slot_party_type, spt_castle),

      # ensure that this center is currently owned by the player's faction
      (store_faction_of_party, ":center_faction", ":center_no"),
      (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
      (eq, ":center_faction", "fac_player_faction"),

      # and that this village has a shrine
      (party_slot_eq, ":center_no", slot_center_has_chapel, 1),

      # keep track of count
      (val_add, ":count", 1),

      # increase the global faithful
      (val_add, "$g_sod_global_faith", "$g_sod_building_chapel_holy"),
      (val_clamp, "$g_sod_global_faith", -2000, 2001),
      (try_begin),
        (gt, "$g_sod_faith", 0),
        (call_script, "script_sod_change_center_faith_support", ":center_no", "$g_sod_faith", "$g_sod_building_chapel_holy"),
      (try_end),

      # Chapels should also steady garrison life and nearby order.
      (party_get_slot, ":center_health", ":center_no", slot_center_sod_local_health),
      (party_get_slot, ":center_prosperity", ":center_no", slot_town_prosperity),
      (party_get_slot, ":food_store", ":center_no", slot_party_food_store),
      (call_script, "script_center_get_food_store_limit", ":center_no"),
      (assign, ":food_store_limit", reg0),
      (try_begin),
        (lt, ":center_health", 58),
        (call_script, "script_change_center_health", ":center_no", 1),
      (try_end),
      (try_begin),
        (lt, ":center_prosperity", 62),
        (store_random_in_range, ":chapel_stability_roll", 0, 100),
        (lt, ":chapel_stability_roll", 20),
        (call_script, "script_change_center_prosperity", ":center_no", 1),
      (try_end),
      (try_begin),
        (gt, ":food_store_limit", 0),
        (store_mul, ":chapel_stable_supply_threshold", ":food_store_limit", 3),
        (val_div, ":chapel_stable_supply_threshold", 5),
        (ge, ":food_store", ":chapel_stable_supply_threshold"),
        (ge, ":center_health", 55),
        (lt, ":center_prosperity", 72),
        (store_random_in_range, ":chapel_cohesion_roll", 0, 100),
        (lt, ":chapel_cohesion_roll", 20),
        (call_script, "script_change_center_prosperity", ":center_no", 1),
      (try_end),

      # let the player know that their efforts are not in vain
      (try_begin),
        (eq, "$g_sod_hide_messages", 0),
        (is_between, "$g_sod_faith", sod_faiths_begin, sod_faiths_end),
        (str_store_party_name_link, s2, ":center_no"),
        (store_add, reg0, "str_sod_chapel_0", "$g_sod_faith"),
        (str_store_string, s1, reg0),
        (display_message, "@The {s1} at {s2} strengthens the faith of the garrison and the folk nearby.", faith_color),
      (try_end),
    (try_end),

    # let the player know that their efforts are not in vain
    (try_begin),
      (eq, "$g_sod_hide_messages", -1),
      (ge, ":count", 1),
      (is_between, "$g_sod_faith", sod_faiths_begin, sod_faiths_end),
      (store_add, reg0, "str_sod_chapel_0", "$g_sod_faith"),
      (str_store_string, s1, reg0),
      (display_message, "@The {s1}s in your castles strengthen faith across your realm.", faith_color),
    (try_end),

    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 1),
    (try_end),
  ]),
]
