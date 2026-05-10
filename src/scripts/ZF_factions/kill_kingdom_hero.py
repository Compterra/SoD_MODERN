SCRIPTS = [
("kill_kingdom_hero",
        [
          (store_script_param_1, ":troop"),

          (try_begin),
            (is_between, ":troop", heroes_begin, heroes_end),
            (call_script, "script_remove_troop_from_prison", ":troop"),
          (try_end),
          (call_script, "script_sod_runtime_trace_event", 5, "$g_enemy_party", ":troop"),
          (troop_set_slot, ":troop", slot_troop_occupation, slto_dead),
          (troop_set_slot, ":troop", slot_troop_leaded_party, -1),

          # store all informations needed to update notes about this lord
          (store_current_day, ":cur_day"),
          (troop_set_slot, ":troop", slot_troop_death_day, ":cur_day"),
          (store_troop_faction, ":troop_faction", ":troop"),
          (try_begin),
            (eq, ":troop_faction", "fac_kingdom_6"),
            (call_script, "script_sod_strategy_advisor_record_centurion_death", ":troop"),
          (try_end),
          (faction_get_slot, ":leader", ":troop_faction", slot_faction_leader),
          (troop_set_slot, ":troop", slot_troop_d_leader, ":leader"),
          (call_script, "script_update_troop_notes", ":troop"),
          (troop_get_type, reg1, ":troop"),
          (str_store_string, s49, "@{reg1?She:He} is dead."),

          (add_troop_note_from_sreg, ":troop", 2, s49, 1),

          # start with the assumption that the fief should return to its faction for redistribution
          (assign, ":fief_faction", ":troop_faction"),

		  (assign, ":best_troop", -1),

          (try_begin),
            # handle executing the King!
            (faction_slot_eq, ":troop_faction", slot_faction_leader, ":troop"),

            # find best candidate to become king
            (try_begin),
              (assign, ":best_troop", -1),
              # Claimants should not inherit by random chance when a king dies.
              # They remain a rebellion path; ordinary succession picks from active lords.
              (try_begin),
                (eq, ":best_troop", -1),
                (assign, ":best_renown", -1),
                (try_for_range, ":candidat", kingdom_heroes_begin, kingdom_heroes_end),
                  (neg|troop_slot_eq, ":candidat", slot_troop_occupation, slto_dead),  #can't choose a dead hero!
                  (neg|is_between, ":candidat", pretenders_begin, pretenders_end),
                  (store_troop_faction, ":faction", ":candidat"),
                  (eq, ":faction", ":troop_faction"),
                  (troop_slot_eq, ":candidat", slot_troop_occupation, slto_kingdom_hero),  #only other heros of this faction may become the king
                  (troop_get_slot, ":renown", ":candidat", slot_troop_renown),
                  (gt, ":renown", ":best_renown"),
                  (assign, ":best_troop", ":candidat"),
                  (assign, ":best_renown", ":renown"),
                (try_end),
              (try_end),

              (try_begin),
                # check if a candidate was found
                (neq, ":best_troop", -1),

                # make them king
                (faction_set_slot, ":troop_faction", slot_faction_leader, ":best_troop"),

                # announce it!
				(call_script, "script_generate_titles"),
                (call_script, "script_store_troop_name_link", s1, ":best_troop"),
                (str_store_faction_name_link, s2, ":troop_faction"),
				(display_log_message, "@{s1} is the new King of the {s2}!", red),
				(assign, "$new_king", ":best_troop"),
				(assign, "$kingdom_with_new_king", ":troop_faction"),
				(assign, "$event_new_king", 1),
              (else_try),
                # all of the lords have been eliminated - so eliminate the faction by making their last fief neutral (q.v. trigger: # Check if a faction is defeated every day)
                (assign, ":fief_faction", "fac_no_faction"),
              (try_end),
            (try_end),
		  (else_try),
			(assign, ":faction_survived", 1),
		  (try_end),


            # free up his fief
            (try_for_range, ":fief", centers_begin, centers_end),
				(party_slot_eq, ":fief", slot_town_lord, ":troop"),
				(try_begin),
					(neq, ":best_troop", -1),
					(party_set_slot, ":fief", slot_town_lord, ":best_troop"),
				(else_try),
					(eq, ":faction_survived", 1),
					(call_script, "script_cf_get_random_lord_of_faction", ":troop_faction"),
					(party_set_slot, ":fief", slot_town_lord, reg0),
				(else_try),
					(party_set_slot, ":fief", slot_town_lord, stl_unassigned),
					(call_script, "script_give_center_to_faction", ":fief", ":fief_faction"),
				(try_end),
			(try_end),

            # remove them from their faction
            (troop_set_slot, ":troop", slot_troop_change_to_faction, "fac_no_faction"),
            (troop_set_slot, ":troop", slot_troop_original_faction, "fac_no_faction"),

            (call_script, "script_update_all_notes"),
        ]),
]
