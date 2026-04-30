SCRIPTS = [
("change_center_health",
        [
          (store_script_param, ":center_no", 1),
          (store_script_param, ":difference", 2),
          (party_get_slot, ":health", ":center_no", slot_center_sod_local_health),
		  (assign, ":max", 101),
		  (try_begin),
			(this_or_next|party_slot_eq, ":center_no", slot_center_has_hospital, 1),
			(party_slot_eq, ":center_no", slot_center_has_ambulatory, 1),
			(val_add, ":max", 20),
		  (try_end),
		  (try_begin),
			(this_or_next|party_slot_eq, ":center_no", slot_center_has_canalization, 1),
			(party_slot_eq, ":center_no", slot_center_has_water_supply, 1),
			(val_add, ":max", 10),
		  (try_end),
			
          (val_clamp, ":health", -100, ":max"),
          (store_add, ":new_health", ":health", ":difference"),
          (val_clamp, ":new_health", -100, ":max"),
          (party_set_slot, ":center_no", slot_center_sod_local_health, ":new_health"),

          # notify the player depending on their desired messages
          (try_begin),
            # only display messages if the player wants them
            (eq, "$g_sod_hide_messages", 0),

            # only announce it for the player's fiefs (or his kingdom's fiefs)
            (store_faction_of_party, ":faction", ":center_no"),
            (this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
            (eq, ":faction", "fac_player_supporters_faction"),

            # only say something if it changed brackets
            (call_script, "script_get_health_bracket", ":health"),
            (assign, ":old_bracket", reg0),
            (call_script, "script_get_health_bracket", ":new_health"),
            (assign, ":new_bracket", reg0),
            (neq, ":new_bracket", ":old_bracket"),

            # generate the message
            (call_script, "script_get_health_text", s1, ":health"),
            (call_script, "script_get_health_text", s2, ":new_health"),
            (str_store_party_name_link, s10, ":center_no"),
            (try_begin),
              (gt, ":new_health", ":health"),
              (display_message, "@{s10} population's health has grown from {s1} to {s2}.", green),
            (else_try),
              (display_message, "@{s10} population's health has declined from {s1} to {s2}.", red),
            (try_end),
          (try_end),
        ]
      ),
]
