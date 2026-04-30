SCRIPTS = [
("setup_troop_meeting",
    [
      (store_script_param_1, ":meeting_troop"),
      (store_script_param_2, ":troop_dna"),
	  # (assign, "$g_sod_member_chat", ":meeting_troop"),
      (modify_visitors_at_site, "scn_conversation_scene"), (reset_visitors),
      (set_visitor, 0, "trp_player"),
      #       (party_stack_get_troop_dna, ":troop_dna", ":meeting_party", 0),
      (set_visitor, 17, ":meeting_troop", ":troop_dna"),
      (set_jump_mission, "mt_conversation_encounter"),
      (jump_to_scene, "scn_conversation_scene"),
      (change_screen_map_conversation, ":meeting_troop"),
  ]),
]
