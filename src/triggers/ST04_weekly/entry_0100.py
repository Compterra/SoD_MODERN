SIMPLE_TRIGGERS = [
(24 * 7,
  [
    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 0),
    (try_end),

    (assign, ":health_pressure_centers", 0),
    (assign, ":health_support_centers", 0),

    # for all centers
    (try_for_range, ":center_no", centers_begin, centers_end),

      # castles don't track faith (chapels are just for faith troop upgrades)
      (neg|is_between, ":center_no", castles_begin, castles_end),

      # only apply religious changes to centers in the players kingdom
      (store_faction_of_party, ":center_faction", ":center_no"),
      (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
      (eq, ":center_faction", "fac_player_faction"),

      (try_begin),
        # and which have at least one religious building...
        (this_or_next|party_slot_eq, ":center_no", slot_center_has_temple, 1),
        (this_or_next|party_slot_eq, ":center_no", slot_center_has_shrine, 1),
        (party_slot_eq, ":center_no", slot_center_has_monastery, 1),
        (party_get_slot, ":cur_faith", ":center_no", slot_center_sod_local_faith),
        (val_clamp, ":cur_faith", -100, 101),
        (party_set_slot, ":center_no", slot_center_sod_local_faith, ":cur_faith"),
        # ...nothing bad happens
      (else_try),
        # Faith now decays faster where the local situation is weak or openly resistant,
        # instead of always dropping by the same flat amount.
        (party_get_slot, ":cur_faith", ":center_no", slot_center_sod_local_faith),
        (assign, ":faith_decay", 1),
        (party_get_slot, ":cur_relation", ":center_no", slot_center_player_relation),
        (party_get_slot, ":center_health", ":center_no", slot_center_sod_local_health),
        (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
        (try_begin),
          (lt, ":cur_relation", 0),
          (val_add, ":faith_decay", 1),
        (try_end),
        (try_begin),
          (this_or_next|lt, ":prosperity", 40),
          (lt, ":center_health", 40),
          (val_add, ":faith_decay", 1),
        (try_end),
        (try_begin),
          (lt, ":cur_faith", -20),
          (val_add, ":faith_decay", 1),
        (try_end),
        (val_min, ":faith_decay", 3),
        (val_sub, ":cur_faith", ":faith_decay"),
        (val_clamp, ":cur_faith", -100, 101),
        (party_set_slot, ":center_no", slot_center_sod_local_faith, ":cur_faith"),
        # inform the player that his lack of a religious building has an impact...
        (try_begin),
          (eq, "$g_sod_hide_messages", 0),
          (is_between, "$g_sod_faith", sod_faiths_begin, sod_faiths_end),
          (str_store_party_name_link, s1, ":center_no"),
          (try_begin),
            (eq, "$g_sod_faith", cb_the_one),
            (display_message, "@{s1}'s faith is lacking for want of a church, monastery, or catheral.", black), #faith_color
          (else_try),
            (eq, "$g_sod_faith", cb_old_gods),
            (display_message, "@{s1}'s faith is lacking for want of a shrine, temple, or grand temple.", black), #faith_color
          (else_try),
            (eq, "$g_sod_faith", cb_the_void),
            (display_message, "@{s1}'s fear is lacking for want of a altar, unholy temple, or temple of pain.", black), #faith_color
          (else_try),
            (eq, "$g_sod_faith", cb_enlightenment),
            (display_message, "@{s1}'s focus is wavering for want of a retreat, meditation grounds, or zen monastery.", black), #faith_color
          (else_try),
            (eq, "$g_sod_faith", cb_atheism),
            (display_message, "@{s1}'s education is lacking for want of a lykeion, schoolhouse, or library.", black), #faith_color
          (try_end),
        (try_end),
      (try_end),

      (party_get_slot, ":center_health", ":center_no", slot_center_sod_local_health),
      (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
      (try_begin),
        (this_or_next|lt, ":center_health", 25),
        (lt, ":prosperity", 30),
        (val_add, ":health_pressure_centers", 1),
      (try_end),
      (try_begin),
        (ge, ":center_health", 65),
        (ge, ":prosperity", 50),
        (val_add, ":health_support_centers", 1),
      (try_end),
    (try_end),

    # Global health should move once per weekly kingdom snapshot, not once per center.
    (try_begin),
      (gt, ":health_pressure_centers", ":health_support_centers"),
      (val_sub, "$g_sod_global_health", 1),
    (else_try),
      (gt, ":health_support_centers", ":health_pressure_centers"),
      (val_add, "$g_sod_global_health", 1),
    (else_try),
      (store_random_in_range, ":rand", 0, 2),
      (try_begin),
        (gt, "$g_sod_global_health", 0),
        (eq, ":rand", 1),
        (val_sub, "$g_sod_global_health", 1),
      (else_try),
        (lt, "$g_sod_global_health", 0),
        (eq, ":rand", 1),
        (val_add, "$g_sod_global_health", 1),
      (try_end),
    (try_end),
    (val_clamp, "$g_sod_global_health", -100, 101),

    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 1),
    (try_end),
  ]),
]
