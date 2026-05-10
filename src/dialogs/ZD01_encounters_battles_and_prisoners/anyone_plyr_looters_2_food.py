DIALOGS = [
[anyone|plyr, "looters_2", [
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (le, ":enemy_size", 12),
    (call_script, "script_get_troop_item_amount", "trp_player", "itm_bread"),
    (assign, ":bread", reg0),
    (call_script, "script_get_troop_item_amount", "trp_player", "itm_dried_meat"),
    (assign, ":meat", reg0),
    (store_add, ":food", ":bread", ":meat"),
    (gt, ":food", 0),
], "Take food and scatter. I will not cut down starving people for sport.", "hostile_food_passage_offer", []],
]
