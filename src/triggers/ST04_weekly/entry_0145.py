SIMPLE_TRIGGERS = [
(24*7,
  [    (try_for_range, ":kingdom_no", native_kingdoms_begin, native_kingdoms_end),
       (faction_slot_eq, ":kingdom_no", slot_faction_state, sfs_active),
		 (assign, ":total_relation_bonus", 0),

		 (faction_get_slot, ":t1", ":kingdom_no", slot_faction_t1_title),
		 (faction_get_slot, ":t2", ":kingdom_no", slot_faction_t2_title),
		 (faction_get_slot, ":t3", ":kingdom_no", slot_faction_t3_title),
		 
		 (assign, ":activate_bonus", 0),
		 
		 (try_for_range, ":kingdom_hero", kingdom_heroes_begin, kingdom_heroes_end),
		 (troop_slot_eq, ":kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
		 (store_troop_faction, ":hero_faction", ":kingdom_hero"),		 
		 (eq, ":hero_faction", ":kingdom_no"),

		 (try_begin),
		 (troop_slot_eq, ":kingdom_hero", slot_troop_player_relation, 0), # probably no interaction with this hero
         (assign, ":relation_with_kingdom_hero", 0),
         (else_try), 		 
		 (call_script, "script_troop_get_player_relation", ":kingdom_hero"),
		 (assign, ":relation_with_kingdom_hero", reg0),
		 (try_end),

		 (store_random_in_range, ":rnd", 0, 50),
			   (try_begin),
				(gt, ":relation_with_kingdom_hero", 3),
				(lt, ":rnd", 48),
				(lt, ":rnd", ":relation_with_kingdom_hero"),
				(assign, ":relation_bonus", 1),
				(assign, ":activate_bonus", 1),
				(else_try),
				(lt, ":relation_with_kingdom_hero", -3),
			    (val_mul, ":relation_with_kingdom_hero", -1),
				(lt, ":rnd", 48),
				(lt, ":rnd", ":relation_with_kingdom_hero"),
				(assign, ":relation_bonus", -1),
				(assign, ":activate_bonus", 1),
				(else_try),
				(assign, ":relation_bonus", 0),
			   (try_end),
			   
			   (troop_get_slot, ":title", ":kingdom_hero", slot_troop_title),

			   (try_begin),
			     (eq, ":title", ":t3"),
                 (val_mul, ":relation_bonus", 2),
                 (else_try),
                 (neq, ":title", ":t1"),    #t4, king or marshall
				 (neq, ":title", ":t2"),
                 (val_mul, ":relation_bonus", 3),
                (try_end),  
				
				(val_add, ":total_relation_bonus", ":relation_bonus"),
			   
		 (try_end),
		 
		 (val_div, ":total_relation_bonus", 2),

         # Safety: this is applied weekly; keep it bounded to avoid runaway drift.
         (val_clamp, ":total_relation_bonus", -10, 11),
		 
		  (try_begin),
		  (eq, ":activate_bonus", 1),
		  (val_sub, ":total_relation_bonus", "$g_sod_diplomatic_difficulty"),				
          (try_end),
         (val_clamp, ":total_relation_bonus", -10, 11),
	
		 (try_begin),
		 (eq, "$g_sod_debug", 1),
		 (assign, reg1, ":total_relation_bonus"),
		 (str_store_faction_name, s6, ":kingdom_no"),
		 (display_message, "@{s6} relation bonus {reg1}", debug_color),
		 (try_end),
		 
		 (store_relation, ":rln", ":kingdom_no", "fac_player_supporters_faction"), 
		 (store_add, ":new_relation", ":rln", ":total_relation_bonus"),
         (val_clamp, ":new_relation", -100, 101),
		 
		 (try_begin),
		   (lt, ":rln", 0),
		   (val_min, ":new_relation", -1),
		 (else_try),
		   (val_max, ":new_relation", 0),
		 (try_end),

		 (call_script, "script_set_player_relation_with_faction", ":kingdom_no", ":new_relation"),
     (try_end),
	 ]),
]
