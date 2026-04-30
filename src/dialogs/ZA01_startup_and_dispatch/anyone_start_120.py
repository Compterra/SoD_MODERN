DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_tavern_talk),
                     (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                     (party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
                     (gt, ":mercenary_amount", 0),
                     (store_sub, reg3, ":mercenary_amount", 1),
                     (store_sub, reg4, reg3, 1),
                     (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                     (assign, ":join_cost", reg0),
                     (store_mul, reg5, ":mercenary_amount", reg0),
                     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                     (val_min, ":mercenary_amount", ":free_capacity"),
                     (store_troop_gold, ":cur_gold", "trp_player"),
                     (try_begin),
                       (gt, ":join_cost", 0),
                       (val_div, ":cur_gold", ":join_cost"),
                       (val_min, ":mercenary_amount", ":cur_gold"),
                     (try_end),
                     (assign, "$temp", ":mercenary_amount"),
                     ],
   "Do you have a need for mercenaries, {sir/madam}?\
 {reg3?Me and {reg4?{reg3} of my mates:one of my mates} are:I am} looking for a master.\
 We'll join you for {reg5} denars.", "mercenary_tavern_talk", []],
]
