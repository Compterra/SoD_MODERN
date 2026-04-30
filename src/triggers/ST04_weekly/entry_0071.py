SIMPLE_TRIGGERS = [
(7 * 24,
   [
       (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
       (store_div, ":renown_decrease", ":player_renown", 200),
       (val_sub, ":player_renown", ":renown_decrease"),
       (troop_set_slot, "trp_player", slot_troop_renown, ":player_renown"),
    ]),
]
