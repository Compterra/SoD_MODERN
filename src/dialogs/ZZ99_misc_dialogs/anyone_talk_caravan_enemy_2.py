DIALOGS = [
[anyone, "talk_caravan_enemy_2", [],
   "Never. It is our duty to protect these goods. You shall have to fight us, brigand!", "close_window",
   [
    (store_relation, ":rel", "$g_encountered_party_faction", "fac_player_supporters_faction"),
    (val_min, ":rel", 0),
    (val_sub, ":rel", 4),
    (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":rel"),
    (call_script, "script_add_log_entry", logent_caravan_accosted, "trp_player",  -1, -1, "$g_encountered_party_faction"),
    ]],
]
