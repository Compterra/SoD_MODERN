DIALOGS = [
[anyone , "knight_join_party_lead_out", [], "Very well then.\
 I shall maintain a patrol of this area. Return if you have further orders for me.", "close_window", [
      (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
      (party_remove_members, "p_main_party", "$g_talk_troop", 1),

      (troop_get_slot, ":companions_party", "$g_talk_troop", slot_troop_leaded_party),
      (party_set_faction, ":companions_party", "fac_player_supporters_faction"),
      (party_detach, ":companions_party"),
      (party_get_position, pos1, ":companions_party"),
      (party_set_ai_behavior, ":companions_party", ai_bhvr_patrol_location),
      (party_set_ai_target_position, ":companions_party", pos1),
      (party_set_ai_patrol_radius, ":companions_party", 5),
      (party_set_slot, ":companions_party", slot_party_ai_state, spai_undefined),
      (party_set_slot, ":companions_party", slot_party_ai_object, -1),
      (party_set_slot, ":companions_party", slot_party_ai_substate, 0),
      (party_set_flags, ":companions_party", pf_default_behavior, 0),
      ]],
]
