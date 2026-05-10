MENUS = [
("kingdom_management", mnf_scale_picture|mnf_enable_hot_keys,
   "What do you want to do?",
   "none",
   [
     (assign, "$g_player_icon_state", pis_normal),
     (set_background_mesh, "mesh_pic_camp"),
    ],
    [
  #SoD fief management
	("sod_fiefmanagement_menu",
        [(eq, "$g_sod_king", 1)],
        "Fief Management.",
        [
		(assign, "$pres_sod_fief_info", 0),
		(assign, "$pres_sod_fief_slider_value", 1),
		(assign, "$pres_sod_fief_selected_building", 1),
		(assign, "$pres_sod_garrison_tip", 0),
		(assign, ":end", centers_end),
		(try_for_range, ":center_no", centers_begin, ":end"),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(assign, ":end", 0),
			(party_get_slot, "$pres_sod_fief_type", ":center_no", slot_party_type),		
			(str_store_party_name, s1, ":center_no"),
			(start_presentation, "prsnt_sod_fief_management"),
		(try_end),
		(try_begin),
			(eq, ":end", centers_end),
			(display_message, "@You have no fiefs!", red),
		(try_end),
       ]
      ),
	#SoD Law
      ("sod_law_menu",
        [(eq, "$g_sod_king", 1)],
        "Realm Laws.",
        [
		(assign, "$law_cur_law", 0),
		(assign, "$law_cur_page", 0),
        (start_presentation, "prsnt_sod_law"),
       ]
      ),
      ("sod_realm_law_report",
        [(eq, "$g_sod_king", 1)],
        "Realm Law Report.",
        [
          (jump_to_menu, "mnu_realm_law_report"),
        ]
      ),
      # SoD Strategic Map feature
      ("camp_strategic",
        [
          (eq, "$g_sod_king", 1)
        ],
        "Strategic Map.",
        [
		  (assign, "$sod_sm_scroll_x", -150),
		  (assign, "$sod_sm_selected_lord", -1),
		  (assign, "$sod_sm_selected_action", -1),
          (start_presentation, "prsnt_strategic_map")
        ]
      ),
	  #SoD Royal Artifacts should be moved somewhere else probably
      ("camp_artifacts",
        [
          (eq, "$g_sod_king", 1)
        ],
        "Royal Artifacts.",
        [
		
		(try_begin),
			(eq, "$g_sod_country", cb_antares),
			(party_count_companions_of_type, ":troop_count1", "p_main_party", "trp_sod_ant_honor_guard"),
			(assign, reg10, ":troop_count1"),
			(assign, "$sod_royal_hero", "trp_sod_ant_honor_guard"),
			(str_store_string, s35, "@Royal artifacts, possesion of your father were stolen after the invasion. They may be anywhere in the lands conquered by The Empire. It's the matter of honour to reclaim them. Choose location on the map, number of troops and mission budget."),
		(else_try),
			(eq, "$g_sod_country", cb_marina),
			(party_count_companions_of_type, ":troop_count1", "p_main_party", "trp_sod_mar_condottieri"),
			(assign, reg10, ":troop_count1"),
			(assign, "$sod_royal_hero", "trp_sod_mar_condottieri"),
			(str_store_string, s35, "@Royal artifacts, possesion of your father were stolen after the invasion. They may be anywhere in the lands conquered by The Empire. It's the matter of honour to reclaim them. Choose location on the map, number of troops and mission budget."),
		(else_try),
		  (eq, "$g_sod_country", cb_aden),
		  (party_count_companions_of_type, ":troop_count1", "p_main_party", "trp_sod_ade_magnate"),
		  (assign, reg10, ":troop_count1"),
		  (assign, "$sod_royal_hero", "trp_sod_ade_magnate"),
		  (str_store_string, s35, "@Royal artifacts, possesion of your father were stolen after the invasion. They may be anywhere in the lands conquered by The Empire. It's the matter of honour to reclaim them. Choose location on the map, number of troops and mission budget."),
		(else_try),
			(eq, "$g_sod_country", cb_villian),
			(party_count_companions_of_type, ":troop_count1", "p_main_party", "trp_sod_vil_high_chief"),
			(assign, reg10, ":troop_count1"),
			(assign, "$sod_royal_hero", "trp_sod_vil_high_chief"),
			(str_store_string, s35, "@Royal artifacts, possesion of your father were stolen after the invasion. They may be anywhere in the lands conquered by The Empire. It's the matter of honour to reclaim them. Choose location on the map, number of troops and mission budget."),
		(else_try),
			(eq, "$g_sod_country", cb_zerrikan),
			(party_count_companions_of_type, ":troop_count1", "p_main_party", "trp_sod_zer_3_noble"),
			(assign, reg10, ":troop_count1"),
			(assign, "$sod_royal_hero", "trp_sod_zer_3_noble"),
			(str_store_string, s35, "@Royal artifacts, possesion of your father were stolen after the invasion. They may be anywhere in the lands conquered by The Empire. It's the matter of honour to reclaim them. Choose location on the map, number of troops and mission budget."),
		(try_end),
			(assign, reg14, 0), #%chance
			(assign, reg13, 0), #mission troops
			(assign, reg12, 1000), #mission founds
			(assign, "$sod_royal_mission", 0),
		#	(assign, reg10, 50), #mission troops in party #TEST REMOVE ME !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			(start_presentation, "prsnt_sod_royal_artifacts")
        ]
      ),
	
      ("resume_travelling", [], "Back.", [(jump_to_menu, "mnu_camp"), ]),
	  
	 ]),
]
