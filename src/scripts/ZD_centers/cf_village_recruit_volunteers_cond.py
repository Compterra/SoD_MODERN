SCRIPTS = [
("cf_village_recruit_volunteers_cond",
        [(neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
          (neg|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
          (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
          (store_faction_of_party, ":village_faction", "$current_town"),
          (party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
          (store_relation, ":village_faction_relation", ":village_faction", "fac_player_faction"),

          (ge, ":center_relation", 0),
          (this_or_next|ge, ":center_relation", 5),
          (this_or_next|eq, ":village_faction", "$players_kingdom"),
          (this_or_next|ge, ":village_faction_relation", 0),
          (this_or_next|eq, ":village_faction", "$supported_pretender_old_faction"),
          (             eq, "$players_kingdom", 0),

          #SOD Population Management Changes Begin
          # limit the number available accorrding to the amount of population above minimum for this village (they can't dig into the minimum required to be a village)
          (party_get_slot, ":volunteers", "$current_town", slot_center_volunteer_troop_amount),
          (party_get_slot, ":population", "$current_town", slot_center_sod_local_population),
          (val_sub, ":population", village_pop_min),
          (val_min, ":volunteers", ":population"),
          (party_set_slot, "$current_town", slot_center_volunteer_troop_amount, ":volunteers"),
          #SOD Population Management Changes End

          (try_begin),
            (eq, "$g_sod_debug", 1),
            (assign, reg0, ":center_relation"),
            (display_message, "@cf_village_recruit_volunteers_cond - village-player relation: {reg0}", debug_color),
            (party_get_slot, reg0, "$current_town", slot_center_volunteer_troop_type),
            (display_message, "@cf_village_recruit_volunteers_cond - troop type: {reg0}", debug_color),
            (party_get_slot, reg0, "$current_town", slot_center_volunteer_troop_amount),
            (display_message, "@cf_village_recruit_volunteers_cond - troop amount: {reg0}", debug_color),
          (try_end),

          (party_slot_ge, "$current_town", slot_center_volunteer_troop_amount, 1), #MORDACHAI- now we won't get the retarded "nobody seems to want to join you..."
          (party_slot_ge, "$current_town", slot_center_volunteer_troop_type, 1),
          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
          (ge, ":free_capacity", 1),
      ]),
]
