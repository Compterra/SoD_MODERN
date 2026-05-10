SCRIPTS = [
("troop_get_player_relation",
    [
      (store_script_param_1, ":troop_no"),
      (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
      (troop_get_slot, ":effective_relation", ":troop_no", slot_troop_player_relation),
      (assign, ":honor_bonus", 0),
	  
      (try_begin),
        (eq,  ":reputation", lrep_quarrelsome),
        (val_add, ":effective_relation", -3),
      (try_end),
	 
	 (try_begin),
        (eq,  ":reputation", lrep_debauched),                   #twan456
		(store_mul, ":honor_bonus", "$player_honor", -1),
		(val_div, ":honor_bonus", 7),
      (try_end),
     
	 (try_begin),
        (ge, "$player_honor", 0),
        (try_begin),
          (this_or_next|eq,  ":reputation", lrep_upstanding),
          (             eq,  ":reputation", lrep_goodnatured),
          (store_div, ":honor_bonus", "$player_honor", 7),
        (try_end),
      (try_end),

      (try_begin),
        (lt, "$player_honor", 0),
			(try_begin),
			  (this_or_next|eq,  ":reputation", lrep_upstanding),
			  (             eq,  ":reputation", lrep_goodnatured),
			  (store_div, ":honor_bonus", "$player_honor", 5),
			(else_try),
			  (eq,  ":reputation", lrep_martial),
			  (store_div, ":honor_bonus", "$player_honor", 8),
			(try_end),
		(try_end),
	  
	  (faction_get_slot, ":badboy", "fac_player_supporters_faction", slot_faction_badboy_rating),
	  (store_troop_faction, ":faction", ":troop_no"),
	  
	  (try_begin),
	    (gt, ":badboy", 15),
		(this_or_next|eq, ":reputation", lrep_upstanding),
		(this_or_next|eq, ":reputation", lrep_goodnatured),
        (eq, ":reputation", lrep_martial),
		(neq, ":faction", "fac_player_supporters_faction"),
		(val_div, ":badboy", 5),
		(val_sub, ":honor_bonus", ":badboy"),
	  (try_end), 	                                         #twan456 end
	  
      (val_add, ":effective_relation", ":honor_bonus"),
      (assign, reg0, ":effective_relation"),
  ]),
]
