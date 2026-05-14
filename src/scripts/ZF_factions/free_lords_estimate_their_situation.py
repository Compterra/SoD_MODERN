SCRIPTS = [
("free_lords_estimate_their_situation",

   [ (call_script, "script_calculate_average_lord_wealth"),
     (call_script, "script_calculate_average_lord_army_strength"),
   
   (try_for_range, ":lord_no", kingdom_heroes_begin, kingdom_heroes_end),
     (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
     (troop_slot_ge, ":lord_no", slot_troop_leaded_party, 1),
	 (neg|is_between, ":lord_no", "trp_black_army_leader_1", kingdom_heroes_end), #twan453 exclude mercenaries
   
    (try_begin),
     (this_or_next|eq, "$g_sod_deactivate_ai",1),
	 (eq, "$g_sod_deactivate_lords_ai", 1),
     (troop_set_slot, ":lord_no", slot_lord_raiding_factor, 100),
     (troop_set_slot, ":lord_no", slot_lord_interception_factor, 100),
     (troop_set_slot, ":lord_no", slot_lord_self_confidence, 100),
	 (troop_set_slot, ":lord_no", slot_lord_initiative, 4),
   (else_try),	 

    (troop_get_slot, ":party", ":lord_no", slot_troop_leaded_party),
	
	(try_begin),
	(party_is_active, ":party"),  #cancel all the calculations if the lord has no party
   
     (call_script, "script_get_number_of_hero_centers", ":lord_no"),
     (assign, ":number_of_centers", reg0),
	 
	 (assign, ":town_lord", 0),
	   (try_for_range, ":town_no", towns_begin, towns_end),
	   (party_slot_eq, ":town_no", slot_town_lord, ":lord_no"),
	   (assign, ":town_lord", 1),
	   (try_end),
	 
     (store_troop_faction, ":faction", ":lord_no"),
     (faction_get_slot, ":ambition", ":faction", slot_faction_ambition),
	 
    (troop_get_slot, ":relative_wealth", ":lord_no", slot_troop_wealth),
    (val_mul, ":relative_wealth", 100),
    (val_max, "$g_average_lord_wealth", 1),
    (val_div, ":relative_wealth", "$g_average_lord_wealth"),
 
    (party_get_slot, ":army_strength", ":party", slot_party_cached_strength),
    (store_mul, ":relative_strength", ":army_strength", 100),
    (val_max, "$g_average_lord_army_strength", 1),
    (val_div, ":relative_strength", "$g_average_lord_army_strength"),

     # RAIDING FACTOR
     (store_sub, ":raiding_factor", 80, ":relative_wealth"),
     (val_mul, ":raiding_factor", 2), # a lord only having 30% of average wealth has doubled chances of raiding, a lord having 130+% of average wealth usually won't raid
     (val_add, ":raiding_factor", 100),
     (assign, ":malus", 0),
     
	 (try_begin),  # strength malus... lords with strong armies have better things to do than killing peasants and very weak lords should prefer to stay in garrisons
     (gt, ":relative_strength", 110),
     (store_sub, ":malus", ":relative_strength", 110),
     (else_try),
     (lt, ":relative_strength", 50),
     (store_sub, ":malus", 50, ":relative_strength"),
     (val_mul, ":malus", 2),
     (try_end),

     (val_sub, ":raiding_factor", ":malus"),
     (val_max, ":raiding_factor", 10),    

     (try_begin),  # raids are the main income of lords with no demesne
     (eq, ":number_of_centers", 0),
	 (val_mul, ":raiding_factor", 3),
     (val_mul, ":raiding_factor", 2),
     (else_try),
     (gt, ":number_of_centers", 1), # when lords with big demesnes or a town don't really need raids
     (val_mul, ":raiding_factor", 2),
	 (store_mul, ":demesne_factor", ":town_lord", 2),
	 (val_add, ":demesne_factor", ":number_of_centers"),
     (val_div, ":raiding_factor", ":demesne_factor"),
     (try_end),

     (try_begin),  # lords of nations with rather low ambition favor raiding as they have small chances to succeed to do other things
     (is_between, ":ambition", -2, 2),
     (val_mul, ":raiding_factor", 4),
     (val_div, ":raiding_factor", 3),
     (else_try),
     (this_or_next|lt, ":ambition", -4), # lords of nations with extreme high or low ambition favor sieging or defense over raiding
     (gt, ":ambition", 4),
     (val_mul, ":raiding_factor", 2),
     (val_div, ":raiding_factor", 3),
     (try_end),

     (try_begin),
     (this_or_next|troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_quarrelsome),
     (troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_debauched),
     (val_mul, ":raiding_factor", 2), # some lords just love to raid villages
     (else_try), 
     (troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_upstanding),
     (val_div, ":raiding_factor", 2),  # some dislike
     (else_try),
     (troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_goodnatured),
     (val_div, ":raiding_factor", 10), # and some are really against that 
     (try_end),

     (troop_get_slot, ":sod_pay_strain", ":lord_no", slot_troop_sod_lord_pay_strain),
     (try_begin),
       (ge, ":sod_pay_strain", 70),
       (val_mul, ":raiding_factor", 3),
       (val_div, ":raiding_factor", 2),
     (else_try),
       (ge, ":sod_pay_strain", 45),
       (val_mul, ":raiding_factor", 6),
       (val_div, ":raiding_factor", 5),
     (try_end),
     (try_begin),
       (troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_cunning),
       (this_or_next|ge, ":sod_pay_strain", 45),
       (lt, ":relative_wealth", 80),
       (val_mul, ":raiding_factor", 5),
       (val_div, ":raiding_factor", 4),
     (try_end),

     (troop_set_slot, ":lord_no", slot_lord_raiding_factor, ":raiding_factor"),

     # INITIATIVE
     # the higher initiative is the more a lord value his own position compared to his kingdom central center and objective
     # it makes lord with big armies and serving ambitious nations behave more like vanilla lords, and sometimes siege castles far from national objectives

	 (assign, ":initiative", 0),
	 
     (try_begin),
	 (gt, ":relative_strength", 275),
	 (assign, ":initiative", 7),
	 (else_try),
     (gt, ":relative_strength", 200),
     (assign, ":initiative", 6),
     (else_try),
     (this_or_next|gt, ":relative_strength", 150),
	 (troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_selfrighteous), # some lords are more adventurous than average and always behave like if they have a strong army
     (assign, ":initiative", 5),
     (else_try),
     (gt, ":relative_strength", 125),
     (assign, ":initiative", 4),
	 (else_try),
	 (gt, ":relative_strength", 105),
	 (assign, ":initiative", 3),
     (else_try),
     (gt, ":relative_strength", 80),
     (assign, ":initiative", 2),
     (else_try),
	 (gt, ":relative_strength", 60),
     (assign, ":initiative", 1),
     (try_end),
     
     (try_begin), # lords with no center are the most likely to travel far from homeland searching villages to raid or places they can take by themselves
     (eq, ":number_of_centers", 0),
     (val_add, ":initiative", 2),
     (try_end),

     (try_begin),
     (troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_martial), # the most common kind of lords don't take too much initiatives
     (val_sub, ":initiative", 1),
     (try_end),
     
     (try_begin),
     (this_or_next|gt, ":ambition", 3),
     (troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_debauched),  # some lords ignore the situation of their realm 
	 (val_add, ":initiative", 2),
     (else_try),
     (gt, ":ambition", 1),
     (val_add, ":initiative", 1),
     (else_try),
     (lt, ":ambition", -2),
     (val_sub, ":initiative", 1),
     (try_end),

     (troop_get_slot, ":readiness", ":lord_no", slot_troop_readiness_to_join_army),
     (try_begin),
     (gt, ":readiness", 60),
     (val_sub, ":initiative", 1),  # lords ready to join army are less likely to take initiatives (contrary is true)
	 (else_try),
	 (lt, ":readiness", 25),
	 (val_add, ":initiative", 1),
     (try_end),
	 
	 (store_random_in_range, ":rnd", -1, 2), # a little random variation for the lord's mood
     (val_add, ":initiative", ":rnd"),
	 
	 (try_begin),                       #twan453 make 1/10 of the invaders with good armies scout far from legion objective
	 (eq, ":faction", "fac_kingdom_6"),
	 (ge, ":relative_strength", 80),
	 (store_random_in_range, ":rnd", 0, 10),
	 (eq, ":rnd", 0),
	 (assign, ":initiative", 10),
	 (party_set_slot, ":party", slot_party_commander_party, -1),
	 (try_end),                       #twan453 end
	 
     (troop_get_slot, ":sod_lord_morale", ":lord_no", slot_troop_sod_lord_party_morale),
     (troop_get_slot, ":sod_fatigue", ":lord_no", slot_troop_sod_lord_campaign_fatigue),
     (troop_get_slot, ":sod_supply", ":lord_no", slot_troop_sod_lord_supply_confidence),
     (try_begin),
       (is_between, ":sod_lord_morale", 1, 40),
       (val_sub, ":initiative", 2),
     (else_try),
       (is_between, ":sod_lord_morale", 40, 60),
       (val_sub, ":initiative", 1),
     (else_try),
       (ge, ":sod_lord_morale", 80),
       (val_add, ":initiative", 1),
     (try_end),
     (try_begin),
       (ge, ":sod_fatigue", 70),
       (val_sub, ":initiative", 1),
     (try_end),
     (try_begin),
       (is_between, ":sod_supply", 1, 30),
       (val_sub, ":initiative", 1),
     (else_try),
       (ge, ":sod_supply", 75),
       (val_add, ":initiative", 1),
     (try_end),
	 (val_clamp, ":initiative", 0, 9),
     (troop_set_slot, ":lord_no", slot_lord_initiative, ":initiative"),

     # READINESS TO JOIN ARMY
     # standard readiness decay is 1 by 10 hours when a lord follow marshall, so a bonus of 1 means 1/3 slower decay 

     (try_begin),
     (lt, ":relative_strength", 30),   # lords with the weakest armies tend to stay/return home instead of following the marshall
     (assign, ":readiness_bonus", -2), # twan new
     (else_try),                       
     (lt, ":relative_strength", 50),
     (assign, ":readiness_bonus", -1),
     (else_try),
     (is_between, ":relative_strength", 70, 90),  # lords with a little under average armies are the more likely to follow the marshall as it would be risky to try to do things alone
     (lt, ":raiding_factor", 150),                # (except if they need to raid villages)
     (assign, ":readiness_bonus", 2),
     (else_try),
     (lt, ":relative_strength", 105),
     (lt, ":raiding_factor", 150),
     (assign, ":readiness_bonus", 1),
     (else_try),
     (is_between, ":relative_strength", 120, 160),  # lords with strong armies usually tend to do things by themselves instead of staying in the army when the situation is good 
     (gt, ":ambition", 1),                          # but are more likely to join the marshall if their kingdom is in a bad situation
     (assign, ":readiness_bonus", -2),
     (else_try),
     (is_between, ":relative_strength", 120, 160),  
     (lt, ":ambition", -2),
     (assign, ":readiness_bonus", 2),
     (else_try),
     (ge, ":relative_strength", 160),
     (gt, ":ambition", 0),
     (assign, ":readiness_bonus", -3),
     (else_try),
     (ge, ":relative_strength", 160),
     (lt, ":ambition", -2),
     (assign, ":readiness_bonus", 3),
     (try_end),

     (try_begin),
     (this_or_next|troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_martial), # the most common kind of lords is the good soldier type
     (this_or_next|troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_upstanding), # and some others have a high sense of duty
	 (troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_quarrelsome), #or just love war
	 (val_add, ":readiness_bonus", 1),
     (else_try),
     (this_or_next|troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_debauched), # but some don't like to follow orders
     (troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_selfrighteous), 
     (val_min, ":readiness_bonus", 0),
     (try_end),
    
     (party_get_slot, ":commander_party", ":party", slot_party_commander_party),

     (try_begin),
     (assign, ":has_valid_commander", 0),
     (try_begin),
       (eq, ":commander_party", "p_main_party"),
       (eq, ":faction", "$players_kingdom"),
       (assign, ":has_valid_commander", 1),
     (else_try),
       (gt, ":commander_party", 0),
       (party_is_active, ":commander_party"),
       (assign, ":has_valid_commander", 1),
     (try_end),
     (eq, ":has_valid_commander", 1),   # lord already in the army
	 (val_sub, ":readiness_bonus", 1),
     (val_min, ":readiness_bonus", 2),   #a bonus of 3 would mean no readiness decay at all
     (try_end),             

     (try_begin),
       (is_between, ":sod_lord_morale", 1, 20),
       (val_sub, ":readiness_bonus", 3),
     (else_try),
       (is_between, ":sod_lord_morale", 20, 40),
       (val_sub, ":readiness_bonus", 2),
     (else_try),
       (is_between, ":sod_lord_morale", 40, 60),
       (val_sub, ":readiness_bonus", 1),
     (else_try),
       (ge, ":sod_lord_morale", 80),
       (val_add, ":readiness_bonus", 1),
     (try_end),
     (try_begin),
       (is_between, ":sod_lord_morale", 20, 60),
       (lt, ":relative_strength", 105),
       (lt, ":sod_fatigue", 55),
       (lt, ":sod_pay_strain", 55),
       (val_add, ":readiness_bonus", 2),
     (try_end),
     (try_begin),
       (ge, ":sod_fatigue", 70),
       (val_sub, ":readiness_bonus", 2),
     (else_try),
       (ge, ":sod_fatigue", 45),
       (val_sub, ":readiness_bonus", 1),
     (try_end),
     (try_begin),
       (ge, ":sod_pay_strain", 70),
       (val_sub, ":readiness_bonus", 2),
     (else_try),
       (ge, ":sod_pay_strain", 45),
       (val_sub, ":readiness_bonus", 1),
     (try_end),
     (try_begin),
       (is_between, ":sod_supply", 1, 30),
       (val_sub, ":readiness_bonus", 1),
     (else_try),
       (ge, ":sod_supply", 75),
       (val_add, ":readiness_bonus", 1),
     (try_end),
     (try_begin),
       (troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_quarrelsome),
       (lt, ":sod_lord_morale", 50),
       (val_sub, ":readiness_bonus", 1),
     (try_end),
    
     (troop_get_slot, ":readiness_orders", ":lord_no", slot_troop_readiness_to_follow_orders),
     (val_add, ":readiness", ":readiness_bonus"),
     (val_add, ":readiness_orders", ":readiness_bonus"),
	 
	 (try_begin),        #twan453 give 0 readiness to half the invaders scouts and 5% of other invaders so they do things alone, give random readiness >15 to 30% of the invaders having less than 15
	 (eq, ":faction", "fac_kingdom_6"),
	 (store_random_in_range, ":rnd", 0, 20),
		 (try_begin),
		 (lt, ":rnd", 10),
		 (eq, ":initiative", 10),
		 (assign, ":readiness", 0),
		 (else_try),
		 (eq, ":rnd", 0),
		 (assign, ":readiness", 0),
		 (else_try),
		 (lt, ":rnd", 6),
		 (lt, ":readiness", 15),
		 (ge, ":relative_strength", 60),    # only when they have armies
		 (store_random_in_range, ":readiness", 15, 100),
		 (try_end),
	 (try_end),       #twan453 end   
	 
     (val_clamp, ":readiness", 0, 100),
     (val_clamp, ":readiness_orders", 0, 100),
     (troop_set_slot, ":lord_no", slot_troop_readiness_to_join_army, ":readiness"),
     (troop_set_slot, ":lord_no", slot_troop_readiness_to_follow_orders, ":readiness_orders"),

     # INTERCEPTION FACTOR
     # the better a lord army is for open battles, the more the lord will patrol (for the marshall also make him more likely to attack armies)
     # interception factor is used to determine garrisoning factor in the AI script (200-interception_factor)
	 
	 (call_script, "script_party_calculate_siege_or_not_strength", ":party", 0),
	 (assign, ":outdoor_strength", reg0),
	 (call_script, "script_party_calculate_siege_or_not_strength", ":party", 1),
	 (assign, ":siege_strength", reg0),
	 
     (val_mul, ":outdoor_strength", 110), # siege strength is usually a little greater
	 (store_div, ":interception_factor", ":outdoor_strength", ":siege_strength"),

     (try_begin),
     (troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_quarrelsome),  # some lords like/dislike open battles
     (val_mul, ":interception_factor", 5),
     (val_div, ":interception_factor", 4),
     (else_try),
     (troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_cunning),
     (val_mul, ":interception_factor", 4),
     (val_div, ":interception_factor", 5),
     (try_end),
     (try_begin),
       (ge, ":sod_lord_morale", 80),
       (ge, ":relative_strength", 90),
       (val_mul, ":interception_factor", 6),
       (val_div, ":interception_factor", 5),
     (else_try),
       (is_between, ":sod_lord_morale", 1, 40),
       (val_mul, ":interception_factor", 4),
       (val_div, ":interception_factor", 5),
     (try_end),
	 
	 (val_clamp, ":interception_factor", 70, 130), # avoid to see specialized factions patrol all the time or never patrol (out of special circonstances)
	

     (call_script, "script_get_number_of_factions_at_war_with_faction", ":faction"),	
	 (try_begin),
     (eq, reg0, 0),
     (val_mul, ":interception_factor", 2), # lords of kingdom at peace chase bandits more often
	 (else_try),
     (this_or_next|ge, ":ambition", 3),  # kingdoms at war and in extremely good or bad situations prefer to have their lords sieging or garrisoning castles than patrolling
     (le, ":ambition", -3),
     (val_mul, ":interception_factor", 3),
     (val_div, ":interception_factor", 4),
     (try_end),
	 
	 (try_begin),
	 (lt, ":relative_strength", 40),           # lords with really weak armies prefer to stay inside the castles
	 (val_div, ":interception_factor", 2), 
	 (else_try),
	 (lt, ":relative_strength", 55),
	 (val_div, ":interception_factor", 3),
	 (val_mul, ":interception_factor", 2),
     (try_end),
	 
	 (try_begin),   #twan453 make 3/4 the invaders with 0 readiness and not scouting far more likely to garrison or siege, as well 10% of other invaders and 5% likely to patrol
	 (eq, ":faction", "fac_kingdom_6"),
	 (ge, ":relative_strength", 80),
	 (store_random_in_range, ":rnd", 0, 20),
	   (try_begin),
	   (eq, ":readiness", 0),
	   (lt, ":initiative", 10),
	   (lt, ":rnd", 15),
	   (val_div, ":interception_factor", 4),
	   (else_try),
	   (eq, ":readiness", 0),
	   (lt, ":initiative", 10),
	   (val_mul, ":interception_factor", 2),
	   (else_try),
	   (eq, ":rnd", 0),
	   (val_mul, ":interception_factor", 2),
	   (else_try),
	   (lt, ":rnd", 3),
	   (val_div, ":interception_factor", 2),
	   (try_end),
	 (try_end),                       #twan453 end
	 
     (troop_set_slot, ":lord_no", slot_lord_interception_factor, ":interception_factor"),

     
     # SELF CONFIDENCE
     # adjust how a lord evaluate his own army strength especially in sieges (lords take more risks when they are rich and may easily replace their armies) 

     (store_mul, ":self_confidence", ":relative_wealth", 2),
     (val_add, ":self_confidence", ":relative_strength"),
     (store_mul, ":bonus_percent", ":ambition", ":number_of_centers"),
     (val_mul, ":bonus_percent", 4),
     (store_random_in_range, ":random_bonus", -10, 11),
     (val_add, ":bonus_percent", ":random_bonus"),
     (val_add, ":bonus_percent", 100),
     (val_mul, ":self_confidence", ":bonus_percent"),
     (val_div, ":self_confidence", 300),
     
     (val_add, ":self_confidence", 100),
     (val_div, ":self_confidence", 2),   # mitigation

     (try_begin),
     (troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_upstanding), # pragmatic lords estimate their forces more correctly
     (val_clamp, ":self_confidence", 90, 110),
     (else_try), 
	 (troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_cunning), # some have a prudent nature
	 (val_min, ":self_confidence", 100),
	 (else_try),
     (this_or_next|troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_selfrighteous), # when some personnality types, town lords and rulers tend to always overestimate their armies
     (this_or_next|troop_slot_eq, ":lord_no", slot_lord_reputation_type, lrep_quarrelsome),
	 (this_or_next|eq, ":town_lord", 1),
     (faction_slot_eq, ":faction", slot_faction_leader, ":lord_no"),
     (val_add, ":self_confidence", 15),
     (val_max, ":self_confidence", 110),	 
     (try_end),
     
     (try_begin),
     (gt, ":relative_strength", 40),  # self confidence make powerful lords more likely to assault castles than in vanilla and poor more prudent but shouldn't be extreme for them	 
     (val_clamp, ":self_confidence", 70, 130), 
     (try_end),	 

     (troop_get_slot, ":sod_lord_morale", ":lord_no", slot_troop_sod_lord_party_morale),
     (troop_get_slot, ":sod_pay_strain", ":lord_no", slot_troop_sod_lord_pay_strain),
     (troop_get_slot, ":sod_fatigue", ":lord_no", slot_troop_sod_lord_campaign_fatigue),
     (troop_get_slot, ":sod_supply", ":lord_no", slot_troop_sod_lord_supply_confidence),
     (try_begin),
       (is_between, ":sod_lord_morale", 1, 20),
       (val_sub, ":self_confidence", 35),
     (else_try),
       (is_between, ":sod_lord_morale", 20, 40),
       (val_sub, ":self_confidence", 22),
     (else_try),
       (is_between, ":sod_lord_morale", 40, 60),
       (val_sub, ":self_confidence", 10),
     (else_try),
       (ge, ":sod_lord_morale", 80),
       (val_add, ":self_confidence", 8),
     (try_end),
     (store_div, ":sod_pay_drag", ":sod_pay_strain", 5),
     (store_div, ":sod_fatigue_drag", ":sod_fatigue", 6),
     (val_sub, ":self_confidence", ":sod_pay_drag"),
     (val_sub, ":self_confidence", ":sod_fatigue_drag"),
     (store_sub, ":sod_supply_mod", ":sod_supply", 50),
     (val_div, ":sod_supply_mod", 5),
     (val_add, ":self_confidence", ":sod_supply_mod"),
     (val_clamp, ":self_confidence", 35, 135),
	 
     (troop_set_slot, ":lord_no", slot_lord_self_confidence, ":self_confidence"),

     # PERSONNAL OBJECTIVE
     # used when a lord has high initiative, he will consider the position of his personnal objective and tend to stay in this region 

     (try_begin),
     (gt, ":number_of_centers", 0), # lords with no center have no preference	 
     (troop_get_slot, ":personnal_objective", ":lord_no", slot_lord_personnal_objective),
       (try_begin),
       (is_between, ":personnal_objective", centers_begin, centers_end),
       (store_faction_of_party, ":objective_fac", ":personnal_objective"),
       (store_relation, ":rln", ":objective_fac", ":faction"),
         (try_begin),
         (gt, ":rln", 0),
         (troop_set_slot, ":lord_no", slot_lord_personnal_objective, -1),
         (assign, ":personnal_objective", -1),
         (try_end),
       (try_end),
       (try_begin),
       (gt, ":personnal_objective", 0),
       (neg|is_between, ":personnal_objective", centers_begin, centers_end),
       (troop_set_slot, ":lord_no", slot_lord_personnal_objective, -1),
       (assign, ":personnal_objective", -1),
       (try_end),
       (try_begin),
       (le, ":personnal_objective", 0),
       (ge, ":initiative", 3),
       (call_script, "script_lord_set_his_personnal_objective", ":lord_no", ":number_of_centers"),
       (try_end),
     (try_end),
     
     #DEBUG 
	 (try_begin),
	 (eq, "$g_sod_debug", 1),
     (assign, reg0, ":raiding_factor"),
     (assign, reg1, ":interception_factor"),
     (assign, reg2, ":initiative"),
     (assign, reg3, ":relative_strength"),
     (assign, reg4, ":army_strength"),
	 (assign, reg5, ":relative_wealth"),
     (str_store_troop_name, s5, ":lord_no"),
     (display_log_message, "@{s5} Raiding factor {reg0} Interception {reg1} Initiative {reg2} RelStr {reg3} RelWealth {reg5} ArmyStr {reg4}", debug_color),
     (try_end),

     (try_end),     # end party is active
     (try_end),     # end deactivate lords ai
	 (try_end),     # end try for range
     ]),
]
