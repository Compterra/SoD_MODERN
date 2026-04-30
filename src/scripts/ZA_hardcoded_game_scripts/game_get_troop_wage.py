SCRIPTS = [
("game_get_troop_wage",
    [
      (store_script_param_1, ":troop_id"),
      (store_script_param_2, ":unused"), #party id

      (assign, ":wage", 0),
      (try_begin),
        (this_or_next|eq, ":troop_id", "trp_player"),
        (this_or_next|eq, ":troop_id", "trp_sod_strategy_advisor"),
        (this_or_next|eq, ":troop_id", "trp_kingdom_6_lord"),
        (eq, ":troop_id", "trp_kidnapped_girl"),
      (else_try),
        (is_between, ":troop_id", pretenders_begin, pretenders_end),
      (else_try),
        (store_character_level, ":troop_level", ":troop_id"),
        (assign, ":wage", ":troop_level"),
        (val_add, ":wage", 3),
        (val_mul, ":wage", ":wage"),
        (val_div, ":wage", 25),
      (try_end),

      (try_begin), #mounted troops cost 65% more than the normal cost
        (troop_is_mounted, ":troop_id"),
        (val_mul, ":wage", 5),
        (val_div, ":wage", 3),
      (try_end),

      (try_begin), #mercenaries cost %50 more than the normal cost
        (this_or_next|is_between, ":troop_id", mercenary_troops_begin, mercenary_troops_end),
        (is_between, ":troop_id", "trp_khergit_tribesman", "trp_ief_deserter"),
        (val_mul, ":wage", 3),
        (val_div, ":wage", 2),
      (try_end),
	  (try_begin),
		(store_troop_faction, ":fac", ":troop_id"),
		(faction_slot_eq, ":fac", slot_guild_noble, ":troop_id"),
        (val_mul, ":wage", 3),
        (val_div, ":wage", 2),
	  (try_end),
      (try_begin),
        # heros cost 200%
        (is_between, ":troop_id", companions_begin, companions_end),
        (val_mul, ":wage", 2),
      (try_end),
	  
	  
	  #pact with mercenary guild gives 25% discount
	  (try_begin),
		(store_troop_faction, ":fac", ":troop_id"),
		(faction_slot_eq, "fac_player_supporters_faction", slot_faction_merc_pact, ":fac"),
		(val_mul, ":wage", 3),
		(val_div, ":wage", 4),
	  (try_end),

      (store_skill_level, ":leadership_level", "skl_leadership", "trp_player"),
      (store_mul, ":leadership_bonus", leadership_discount_multiplier, ":leadership_level"),
      (store_sub, ":leadership_factor", 100, ":leadership_bonus"),
      (val_mul, ":wage", ":leadership_factor"),  #wage = wage * (100 - 5*leadership)/100
      (val_div, ":wage", 100),

      (try_begin),
        (neq, ":troop_id", "trp_player"),
        (neq, ":troop_id", "trp_kidnapped_girl"),
        (neq, ":troop_id", "trp_sod_strategy_advisor"),
        (neq, ":troop_id", "trp_kingdom_6_lord"),
        (neg|is_between, ":troop_id", pretenders_begin, pretenders_end),
        (val_max, ":wage", 1),
      (try_end),

      (assign, reg0, ":wage"),
      (set_trigger_result, reg0),
  ]),
]
