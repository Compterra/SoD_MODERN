MENUS = [
(
    "town_speak_with_reps", mnf_enable_hot_keys,
    "You're at {s1}.^^Which guild representative do you wish to speak with?",
    "none",
    [
      (set_background_mesh, "$g_sod_town_background"),
      (assign, "$talk_context", tc_court_talk),

      (set_jump_mission, "mt_visit_town_castle"),
      (set_passage_menu, "mnu_town_castle_passages"),
      (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
      (modify_visitors_at_site, ":castle_scene"),
      (reset_visitors),
      #Adding guards
      (store_faction_of_party, ":center_faction", "$current_town"),
      (faction_get_slot, ":guard_troop", ":center_faction", slot_faction_guard_troop),
      (try_begin),
        (le, ":guard_troop", 0),
        (assign, ":guard_troop", "trp_swadian_sergeant"),
      (try_end),
      (set_visitor, 6, ":guard_troop"),
      (set_visitor, 7, ":guard_troop"),
	  
      #SoD COURT BEGIN
      (try_begin),
        (this_or_next|eq, ":center_faction", "fac_player_faction"),
        (eq, ":center_faction", "fac_player_supporters_faction"),
        (set_visitor, 17, "trp_sod_marshal"),
        (set_visitor, 18, "trp_sod_chancellor"),
        (set_visitor, 19, "trp_sod_treasurer"),
        (troop_set_slot, "trp_sod_marshal", slot_troop_sod_court, "$current_town"), #SoD ARMY MANAGEMENT
		(try_begin),
			(eq, "$g_sod_sa_in_court", 1),
			(set_visitor, 20, "trp_sod_strategy_advisor"),
		(try_end),
      (try_end),
	  (try_begin),
        (neq, ":center_faction", "fac_player_supporters_faction"),
		(faction_get_slot, ":leader", ":center_faction", slot_faction_leader),
		(party_slot_eq, "$current_town", slot_town_lord, ":leader"),
		(faction_get_slot,":m_guild", ":center_faction", slot_faction_merc_pact),
		(gt, ":m_guild", 0),
		(faction_get_slot,":representative", ":m_guild", slot_guild_representative),
		(set_visitor, 17, ":representative"),
	  (try_end),
      #SoD COURT END
	  (try_begin),
	    (this_or_next|eq, "$cheat_mode", 1),
	    (eq, "$g_sod_cheat_mode", 1),
	    (set_visitor, 16, "trp_sod_jester"),
	  (try_end),
      #SoD following was changed from (assign, ":cur_pos", 16),
	  
      (try_begin),
        (eq, ":center_faction", "fac_player_supporters_faction"),
		(assign, ":cur_pos", 21),
		(try_for_range, ":guild", guilds_begin, guilds_end),
			(store_relation, ":rel", "fac_player_faction", ":guild"),
			(ge, ":rel", 30),
			(faction_get_slot,":representative", ":guild", slot_guild_representative),
			(set_visitor, ":cur_pos", ":representative"),
			(val_add, ":cur_pos", 1),
		(try_end),
		(try_begin),
			(store_relation, ":rel", "fac_player_faction", "fac_commoners"),
			(ge, ":rel", 30),
			(set_visitor, ":cur_pos", ransom_brokers_begin),
			(val_add, ":cur_pos", 1),
		(try_end),
	  (else_try),
		(assign, ":cur_pos", 18),
	  (try_end),
	  
      (call_script, "script_get_heroes_attached_to_center", "$current_town", "p_temp_party"),
      (party_get_num_companion_stacks, ":num_stacks", "p_temp_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":i_stack"),
        (lt, ":cur_pos", 32), # spawn up to entry point 32
        (set_visitor, ":cur_pos", ":stack_troop"),
        (val_add, ":cur_pos", 1),
      (try_end),
      (try_for_range, ":cur_troop", heroes_begin, heroes_end),
        (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_lady),
        (troop_slot_eq, ":cur_troop", slot_troop_cur_center, "$current_town"),
        (lt, ":cur_pos", 32), # spawn up to entry point 32
        (set_visitor, ":cur_pos", ":cur_troop"),
        (val_add, ":cur_pos", 1),
      (try_end),
	  
      (str_store_party_name, s1, "$current_town"),
    ],
    [
      ("talk_council_rep_0", [
			(store_relation, ":rel", "fac_player_faction", "fac_commoners"),
			(ge, ":rel", 30),
	  ], "Ransom Broker.",
        [
          (set_jump_mission, "mt_visit_town_castle"),
          (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
          (jump_to_scene, ":castle_scene"),
          (change_screen_map_conversation, ransom_brokers_begin),
        ]
      ),
      ("talk_council_rep_1", [
			(store_relation, ":rel", "fac_player_faction", "fac_sod_merc_guild1"),
			(ge, ":rel", 30),
	  ], "Black Army Representative.",
        [
          (set_jump_mission, "mt_visit_town_castle"),
          (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
          (jump_to_scene, ":castle_scene"),
          (change_screen_map_conversation, black_army_rep),
        ]
      ),
      ("talk_council_rep_2", [
			(store_relation, ":rel", "fac_player_faction", "fac_sod_merc_guild2"),
			(ge, ":rel", 30),
	  ], "Conquistadors Representative.",
        [
          (set_jump_mission, "mt_visit_town_castle"),
          (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
          (jump_to_scene, ":castle_scene"),
          (change_screen_map_conversation, conquistadors_rep),
        ]
      ),
      ("talk_council_rep_3", [
			(store_relation, ":rel", "fac_player_faction", "fac_sod_merc_guild3"),
			(ge, ":rel", 30),
	  ], "Elephant Guard Representative.",
        [
          (set_jump_mission, "mt_visit_town_castle"),
          (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
          (jump_to_scene, ":castle_scene"),
          (change_screen_map_conversation, elephant_guard_rep),
        ]
      ),
      ("talk_council_rep_4", [
			(store_relation, ":rel", "fac_player_faction", "fac_sod_merc_guild4"),
			(ge, ":rel", 30),
	  ], "Jotnar Clan Representative.",
        [
          (set_jump_mission, "mt_visit_town_castle"),
          (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
          (jump_to_scene, ":castle_scene"),
          (change_screen_map_conversation, jotnar_clan_rep),
        ]
      ),
      ("talk_council_rep_5", [
			(store_relation, ":rel", "fac_player_faction", "fac_sod_merc_guild5"),
			(ge, ":rel", 30),
	  ], "Serpent Host Representative.",
        [
          (set_jump_mission, "mt_visit_town_castle"),
          (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
          (jump_to_scene, ":castle_scene"),
          (change_screen_map_conversation, serpent_host_rep),
        ]
      ),
      ("talk_council_rep_6", [
			(store_relation, ":rel", "fac_player_faction", "fac_sod_merc_guild6"),
			(ge, ":rel", 30),
	  ], "Slavers Representative.",
        [
          (set_jump_mission, "mt_visit_town_castle"),
          (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
          (jump_to_scene, ":castle_scene"),
          (change_screen_map_conversation, slavers_rep),
        ]
      ),
      ("talk_council_return", [], "That will be all.", [(jump_to_menu, "mnu_town")]),
    ]
  ),
]
