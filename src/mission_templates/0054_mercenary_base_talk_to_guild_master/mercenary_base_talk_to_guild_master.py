MISSION_TEMPLATES = [
(
    "mercenary_base_talk_to_guild_master", 0, -1,
    "Default mercenary base visit.",
    [(0,mtef_scene_source,0,0,1,[]),
    (10,mtef_scene_source,af_override_horse,0,1,[]),
	
	(1,mtef_visitor_source,af_override_horse,0,1,[]),
	(2,mtef_visitor_source,af_override_horse,0,1,[]),
	(3,mtef_visitor_source,af_override_horse,0,1,[]),
	(4,mtef_visitor_source,af_override_horse,0,1,[]),
	(5,mtef_visitor_source,af_override_horse,0,1,[]),
	(6,mtef_visitor_source,af_override_horse,0,1,[]),
	(7,mtef_visitor_source,af_override_horse,0,1,[]),
	(8,mtef_visitor_source,af_override_horse,0,1,[]),
	(9,mtef_visitor_source,af_override_horse,0,1,[]),
	
	(11,mtef_visitor_source,af_override_horse,0,1,[]),	
	(12,mtef_visitor_source,af_override_horse,0,1,[]),
	(13,mtef_visitor_source,af_override_horse,0,1,[]),
	(14,mtef_visitor_source,af_override_horse,0,1,[]),
	(15,mtef_visitor_source,af_override_horse,0,1,[]),
	(16,mtef_visitor_source,af_override_horse,0,1,[]),
	(17,mtef_visitor_source,af_override_horse,0,1,[]),
	(18,mtef_visitor_source,af_override_horse,0,1,[]),
	(19,mtef_visitor_source,af_override_horse,0,1,[]),
	(20,mtef_visitor_source,af_override_horse,0,1,[]),
	
	(30,mtef_scene_source,af_override_horse,0,1,[]),
   	 ],
	 [
	 (1, 0, ti_once, [], [
       (start_mission_conversation, "$g_talk_troop"),
        ]),
		
      (ti_tab_pressed, 0, 0, [(set_trigger_result, 1)], [(assign, "$fight_guild_troops_quest", -1)]),
	  ],
    ),
]
