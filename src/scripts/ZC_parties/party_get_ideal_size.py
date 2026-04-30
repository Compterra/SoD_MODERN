SCRIPTS = [
("party_get_ideal_size",
    [
      (store_script_param_1, ":party_no"),
      (assign, ":limit", 30),
      (try_begin),
        (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
        (party_stack_get_troop_id, ":party_leader", ":party_no", 0),
        (store_faction_of_party, ":faction_id", ":party_no"),
        (assign, ":limit", 10),

        (store_skill_level, ":skill", "skl_leadership", ":party_leader"),
        (store_attribute_level, ":charisma", ":party_leader", ca_charisma),
        #MORDACHAI - increase troop limit to 10 x leadership skill (was 5x)
        (val_mul, ":skill", 10),
        (val_add, ":limit", ":skill"),
        (val_add, ":limit", ":charisma"),
		
        (try_begin),
          (eq, ":faction_id", "fac_player_supporters_faction"),
          (val_add, ":limit", "$g_sod_lord_party_size_modifier"), #from laws
        (else_try),
          (faction_get_slot, ":law_party_size", ":faction_id", slot_faction_law_lord_party_size_modifier),
          (val_add, ":limit", ":law_party_size"),
        (try_end),
		
        (troop_get_slot, ":troop_renown", ":party_leader", slot_troop_renown),
        (store_div, ":renown_bonus", ":troop_renown", 40),
        (val_add, ":limit", ":renown_bonus"),

        (try_begin),
          (faction_slot_eq, ":faction_id", slot_faction_leader, ":party_leader"),
          (val_add, ":limit", 100),
        (try_end),
      (try_end),
	  
      #SoD let's increase it a bit more
	  (try_begin),
	      (neq, ":faction_id", "fac_player_supporters_faction"),
		  (store_character_level, ":level", "trp_player"), #increase limits a little bit as the game progresses.
		  (val_mul, ":level", 2),
		  (store_add, ":level_factor", 90, ":level"),
		  (val_mul, ":limit", ":level_factor"),
		  (val_div, ":limit", 90),
	  (try_end),
      #SoD Makes NPC party size depend on number of fiefs they have, invaders are not affected BEGIN #################
      #  #####################################################################
      (try_begin),
        (neq, ":faction_id", "fac_kingdom_6"),

        (try_for_range, ":center_no", centers_begin, centers_end),
          (party_slot_eq, ":center_no", slot_town_lord, ":party_leader"),
		  (assign, ":fief_factor", 0),
			  (try_begin),
				(party_slot_eq, ":center_no", slot_party_type, spt_village),
				(val_add, ":fief_factor", 5),
			  (else_try),
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
				(val_add, ":fief_factor", 15),
			  (else_try),
				(party_slot_eq, ":center_no", slot_party_type, spt_town),
				(val_add, ":fief_factor", 20),
			  (try_end),
			  (try_begin),
				(neq, ":faction_id", "fac_player_supporters_faction"),
				(val_mul, ":fief_factor", 2),
			  (try_end),
			(val_add, ":limit", ":fief_factor"),
        (try_end),                                             #twan456 end
      (try_end),
      #SoD END ################################################################
      #  #####################################################################
      (val_max, ":limit", 1),
      (assign, reg0, ":limit"),
  ]),
]
