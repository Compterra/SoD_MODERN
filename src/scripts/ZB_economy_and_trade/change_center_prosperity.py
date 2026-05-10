SCRIPTS = [
("change_center_prosperity",
        [
          (store_script_param, ":center_no", 1),
          (store_script_param, ":difference", 2),

          #SOD: castles don't have prosperity, period!
          (try_begin),
            (is_between, ":center_no", centers_begin, centers_end),
            (neg|is_between, ":center_no", castles_begin, castles_end),

            # only update it if it actually changes
            (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
            (store_add, ":new_prosperity", ":prosperity", ":difference"),
			(assign, ":max", 101),
			(try_begin),
				(this_or_next|party_slot_eq, ":center_no", slot_center_has_mill, 1),
				(party_slot_eq, ":center_no", slot_center_has_guild, 1),
				(val_add, ":max", "$g_sod_building_mill_max_prosperity"),
			(try_end),
			(try_begin),
				(this_or_next|party_slot_eq, ":center_no", slot_center_has_clayworks, 1),
				(party_slot_eq, ":center_no", slot_center_has_manufacture, 1),
				(val_add, ":max", 10),
			(try_end),
            # Use computed :max so buildings can raise prosperity cap above 100.
            (val_clamp, ":new_prosperity", 0, ":max"),
            (neq, ":prosperity", ":new_prosperity"),
            (party_set_slot, ":center_no", slot_town_prosperity, ":new_prosperity"),

            (try_begin),
              (eq, "$g_sod_debug", 1),
              (str_store_party_name_link, s1, ":center_no"),
              (assign, reg1, ":difference"),
              (display_message, "@{s1}'s prosperity has changed by {reg1}.", debug_color),
            (try_end),

            (try_begin),
              # determine if the prosperity bracket has changed
              (call_script, "script_get_prosperity_bracket", ":prosperity"),
              (assign, ":old_state", reg0),
              (call_script, "script_get_prosperity_bracket", ":new_prosperity"),
              (assign, ":new_state", reg0),
              (neq, ":old_state", ":new_state"),

              # update the center notes
              (call_script, "script_update_center_notes", ":center_no"),

              # display a message for the player if their message level requests it
              (try_begin),
                (eq, "$g_sod_hide_messages", 0),

                # only tell the player if this happens in his lands
                (store_faction_of_party, ":center_faction", ":center_no"),
                (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
                (eq, ":center_faction", "fac_player_faction"),

                (str_store_party_name_link, s1, ":center_no"),
                (call_script, "script_get_prosperity_text", s2, ":prosperity"),
                (call_script, "script_get_prosperity_text", s3, ":new_prosperity"),
                (try_begin),
                  (lt, ":prosperity", ":new_prosperity"),
                  (display_message, "@Prosperity of {s1} has improved from {s2} to {s3}.", quest_success_color),
                (else_try),
                  (gt, ":prosperity", ":new_prosperity"),
                  (display_message, "@Prosperity of {s1} has deteriorated from {s2} to {s3}.", quest_fail_color),
                (try_end),
              (try_end),
            (try_end),
          (try_end),
      ]),
]
