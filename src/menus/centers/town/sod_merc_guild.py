MENUS = [
("sod_merc_guild",mnf_disable_all_keys,
  "You approach a mercenary base. Drill sergeants bark orders over the ring of steel, and armed sellswords watch you from the yard as they weigh your purpose here.",
  "none",[
  ],
    [
      ("enter",[],"Step into the yard.",[
	  (assign, "$g_sod_from_menu", 0),
	  (party_get_slot, ":base_scene", "$g_encountered_party", slot_castle_exterior),
	   (assign, "$g_mt_mode", abm_visit),
	   
          (scene_set_slot, ":base_scene", slot_scene_visited, 1),
       (set_jump_mission, "mt_mercenary_base"),
	   (call_script, "script_init_mercenary_base_walkers", ":base_scene"),
	   (jump_to_scene,":base_scene"),(change_screen_mission)],
	   "Door to the courtyard.",
	   ),
	   
	   
      ("office",[
	  (this_or_next|eq, "$g_encountered_party", "p_sod_merc_guild_1"),
	  (this_or_next|eq, "$g_encountered_party", "p_sod_merc_guild_2"),
	  (this_or_next|eq, "$g_encountered_party", "p_sod_merc_guild_3"),
	  (this_or_next|eq, "$g_encountered_party", "p_sod_merc_guild_4"),
	  (eq, "$g_encountered_party", "p_sod_merc_guild_5"),
      ],"Visit the guild master's office.",[
		(assign, "$g_sod_from_menu", -1),
		(party_get_slot, ":base_scene", "$g_encountered_party", slot_town_castle),
		(assign, "$g_mt_mode", abm_visit),
        (scene_set_slot, ":base_scene", slot_scene_visited, 1),
		(set_jump_mission, "mt_mercenary_base_interior"),
		(call_script, "script_init_mercenary_base_walkers", ":base_scene"),
		(jump_to_scene,":base_scene"),(change_screen_mission)],
	   "Door to Guild Master's office.",
	   ),
	   
	   ("talk", [],"Seek an audience with the guild master.", [
		(assign, "$g_sod_from_menu", -1),
       (party_get_slot, ":base_scene", "$g_encountered_party", slot_castle_exterior),
	   (assign, "$g_mt_mode", abm_visit),
       (set_jump_mission, "mt_mercenary_base_talk_to_guild_master"),
	   (store_sub, ":guild_master", "$g_encountered_party", "p_sod_merc_guild_1"),
	   (val_add, ":guild_master", "trp_black_army_guild_master"),
	   (assign, "$g_talk_troop", ":guild_master"),
	   (jump_to_scene,":base_scene"),
	   (change_screen_mission),
		 ]),
	   
	  ("upgrade", [
		 ],
        "Review your soldiers for promotion.",
        [
		  (assign, "$jump_menu", "mnu_sod_merc_guild"),
          (jump_to_menu, "mnu_sod_upgrade"),
        ]
      ),
      
	  ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
  ),
]
