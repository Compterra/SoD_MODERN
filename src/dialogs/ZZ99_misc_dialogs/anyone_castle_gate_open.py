DIALOGS = [
[anyone, "castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
                                         (eq, "$g_encountered_party", reg0),
                                         (ge, "$g_encountered_party_relation", 0),
                                         (call_script, "script_troop_get_player_relation", ":castle_lord"),
                                         (assign, ":castle_lord_relation", reg0),
                                         #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
                                         (ge, ":castle_lord_relation", 5),
                                         (call_script, "script_store_troop_name", s2, ":castle_lord")
                                         ],  "My lord {s2} will be happy to see you {sir/madam}.\
 Come on in. I am opening the gates for you.", "close_window", [(assign, "$g_permitted_to_center", 1)]],
]
