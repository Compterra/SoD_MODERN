SCRIPTS = [
("setup_party_meeting",
    [
      (store_script_param_1, ":meeting_party"),
      (try_begin),
        (lt, "$g_encountered_party_relation", 0), #hostile
        #        (call_script, "script_music_set_situation_with_culture", mtf_sit_encounter_hostile),
      (try_end),
      (party_stack_get_troop_id, ":meeting_troop", ":meeting_party", 0),
      (try_begin),
        (is_between, ":meeting_troop", 0, "trp_last_troop"),
        (modify_visitors_at_site, "scn_conversation_scene"), (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (party_stack_get_troop_dna, ":troop_dna", ":meeting_party", 0),
        (set_visitor, 17, ":meeting_troop", ":troop_dna"),
        (set_jump_mission, "mt_conversation_encounter"),
        (jump_to_scene, "scn_conversation_scene"),
        (change_screen_map_conversation, ":meeting_troop"),
      (try_end),
  ]),
]
