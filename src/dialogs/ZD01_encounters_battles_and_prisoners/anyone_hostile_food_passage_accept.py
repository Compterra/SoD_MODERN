DIALOGS = [
[anyone, "hostile_food_passage_offer", [
    (call_script, "script_get_troop_item_amount", "trp_player", "itm_bread"),
    (assign, ":bread", reg0),
    (call_script, "script_get_troop_item_amount", "trp_player", "itm_dried_meat"),
    (assign, ":meat", reg0),
    (store_add, ":food", ":bread", ":meat"),
    (gt, ":food", 0),
], "Keep your purse then. We will take the food and vanish before your patience changes.", "close_window", [
    (call_script, "script_get_troop_item_amount", "trp_player", "itm_bread"),
    (try_begin),
        (gt, reg0, 0),
        (troop_remove_item, "trp_player", "itm_bread"),
    (else_try),
        (troop_remove_item, "trp_player", "itm_dried_meat"),
    (try_end),
    (call_script, "script_sod_note_hostile_reputation", 1),
    (call_script, "script_sod_resolve_hostile_party_noncombat", "$g_encountered_party"),
]],
]
