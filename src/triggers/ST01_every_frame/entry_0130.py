SIMPLE_TRIGGERS = [
(0.1,
   [
     (try_for_parties, ":cur_party"),
		(this_or_next|party_slot_eq, ":cur_party", slot_party_type, spt_player_mercenaries),
		(party_slot_eq, ":cur_party", slot_party_type, spt_player_patrol),
		(party_get_battle_opponent, ":opponent", ":cur_party"),
        (lt, ":opponent", 0), #party is not involved in a battle
        (party_get_attached_to, ":attached_to", ":cur_party"),
        (lt, ":attached_to", 0), #party is not attached to another party
		(party_get_cur_town, ":destination", ":cur_party"),
        (is_between, ":destination", centers_begin, centers_end),
        (call_script, "script_get_relation_between_parties", ":destination", ":cur_party"),
        (try_begin),
           (ge, reg0, 0),
           (party_attach_to_party, ":cur_party", ":destination"),
		   (try_begin),
				(party_get_num_prisoner_stacks, ":num_stacks", ":cur_party"),
				(gt, ":num_stacks", 0),
				(assign, "$g_move_heroes", 1),
				(call_script, "script_party_prisoners_add_party_prisoners", ":destination", ":cur_party"),
				(call_script, "script_party_remove_all_prisoners", ":cur_party"),
			(try_end),
        (else_try),
           (party_set_ai_behavior, ":cur_party", ai_bhvr_hold),
        (try_end),
	 (try_end),
    ]),
]
