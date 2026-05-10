SIMPLE_TRIGGERS = [
(48,
    [
      # clear the previous attempt to join the player
      (assign, "$g_sod_lord_offers_allegience", 0),

      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 1),
        (neg|troop_slot_ge, ":troop_no", slot_troop_change_to_faction, 1),

        (store_troop_faction, ":cur_faction", ":troop_no"),
        (try_begin),
          (call_script, "script_cf_select_random_walled_center_with_faction_and_owner_priority_no_siege", ":cur_faction", ":troop_no"), #Can fail
          (assign, ":center_no", reg0),
          (call_script, "script_create_kingdom_hero_party", ":troop_no", ":center_no"),
          (party_attach_to_party, "$pout_party", ":center_no"),
        (else_try),  # SoD Twan respawn centurions at the entry point once invasion is started and before the legion gain walled centers
          (eq, ":cur_faction", "fac_kingdom_6"),
          (faction_slot_eq, "fac_kingdom_6", slot_faction_state, sfs_active),
          (faction_get_slot, ":central_center", "fac_kingdom_6", slot_faction_central_center),
          (try_begin),
            (is_between, ":central_center", "p_village_16", "p_village_67"), # only if central center = entry point 
            (troop_set_slot, ":troop_no", slot_troop_spawned_before, 0), #twan456b make them respawn with party 
            (call_script, "script_create_kingdom_hero_party", ":troop_no", ":central_center"),
          (try_end),
        # SoD Twan end (should make harder for the player to block the invasion at the first castle)
      
        (else_try),
          (neg|faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),

          (try_begin),
            # ex-Kings go into retirement...
            (faction_slot_eq, ":cur_faction", slot_faction_leader, ":troop_no"), #twan456 fix new king bug 
            (troop_set_slot, ":troop_no", slot_troop_change_to_faction, "fac_commoners"),
          (else_try),
		    (neq, ":cur_faction", "fac_kingdom_6"),          #MORDACHAI - SOD - keep centurions in limbo until I-day
            # but Lords can change allegience to a still active faction...
            (store_random_in_range, ":random_no", 0, 100),
            (lt, ":random_no", 10), # 10% chance of taking up a new standard

            (try_begin),

              # see if they're amenable to workign for the player (if he has his own kingdom)
              (eq, "$g_sod_king", 1),
              (eq, "$g_sod_lord_offers_allegience", 0), # don't do this if we're currently handling one (one per cycle, max)
              (troop_slot_eq, ":troop_no", slot_lord_allegience_offered, lao_never), # ensure they haven't been rejected in the past

              # % chance to opt for player = (relation - 15)/5 + persuasion + (honor-50)/25
              (troop_get_slot, ":chance", ":troop_no", slot_troop_player_relation),
              (val_sub, ":chance", 15),
              (val_div, ":chance", 5),
              (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
              (val_add, ":chance", ":persuasion"),
              (store_sub, ":honor", "$player_honor", 50),
              (val_div, ":honor", 25),
              (val_add, ":chance", ":honor"),
              (try_begin),
                (eq, "$g_sod_debug", 1),
                # let me know what the computed odds are...
                (assign, reg0, ":chance"),
                (call_script, "script_store_troop_name_link", s1, ":troop_no"),
                (display_message, "@{s1} considers joining you: {reg0}%", gray),
                #(assign, ":chance", 100),
              (try_end),
              (store_random_in_range, reg1, 0, 100),

              # offer allegience to the player (who can still reject)
              (lt, reg1, ":chance"),
              (assign, "$g_sod_lord_offers_allegience", ":troop_no"),
              (troop_set_slot, ":troop_no", slot_lord_allegience_offered, lao_offering),

            (else_try),

              # (try to) choose a realm with land, stability, and room for another lord
              (call_script, "script_sod_lord_choose_patron_faction_to_reg", ":troop_no", ":cur_faction"),
              (assign, ":patron_faction", reg0),
              (assign, ":patron_score", reg1),
              (call_script, "script_sod_claimant_choose_defection_target_to_reg", ":troop_no", ":cur_faction", ":patron_faction"),
              (assign, ":patron_faction", reg0),
              (try_begin),
                (is_between, ":patron_faction", rebel_factions_begin, rebel_factions_end),
                (assign, ":patron_score", reg1),
              (try_end),
              (try_begin),
                (is_between, ":patron_faction", kingdoms_begin, kingdoms_end),
                (neq, ":patron_faction", "fac_player_supporters_faction"),
                (gt, ":patron_score", 35),
                (troop_set_slot, ":troop_no", slot_troop_change_to_faction, ":patron_faction"),
              (else_try),
                (call_script, "script_cf_get_random_active_faction_except_player_faction_and_faction", ":cur_faction"),
                (troop_set_slot, ":troop_no", slot_troop_change_to_faction, reg0),
              (try_end),

            (try_end),
          (try_end),
        (try_end),
      (try_end),

      # have the conversation with the lord offering allegience
      (try_begin),
        (neq, "$g_sod_lord_offers_allegience", 0),
        (start_map_conversation, "$g_sod_lord_offers_allegience"),
      (try_end),
    ]),
]
