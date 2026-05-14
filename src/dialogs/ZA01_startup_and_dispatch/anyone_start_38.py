DIALOGS = [
[anyone, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_player_companion),
                    (gt, "$g_encountered_party", 0),
                    (party_is_active, "$g_encountered_party"),
                    (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
                    (party_get_num_companion_stacks, ":num_stacks", "$g_encountered_party"),
                    (ge, ":num_stacks", 1),
                    (party_stack_get_troop_id, ":castle_leader", "$g_encountered_party", 0),
                    (eq, ":castle_leader", "$g_talk_troop"),
                    (eq, "$talk_context", 0)],
   "Yes, {playername}? What can I do for you?", "member_castellan_talk", []],
]
