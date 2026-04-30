DIALOGS = [
[anyone, "castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                               (call_script, "script_troop_get_player_relation", ":castle_lord"),
                               (assign, ":castle_lord_relation", reg0),
                               #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
                               (ge, ":castle_lord_relation", -19),
                               (call_script, "script_store_troop_name", s2, ":castle_lord")
                                         ],  "Come on in. But make sure your men behave sensibly within the walls.\
 My lord {s2} does not want trouble here.", "close_window", [(assign, "$g_permitted_to_center", 1)]],
]
