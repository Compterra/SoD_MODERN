DIALOGS = [
[anyone , "village_elder_recruit_start", [(party_get_slot, ":num_volunteers", "$current_town", slot_center_volunteer_troop_amount),
                                           (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                           (val_min, ":num_volunteers", ":free_capacity"),
                                           (assign, "$temp",  ":num_volunteers"),
                                           (assign, reg5, ":num_volunteers"),
                                           (store_add, reg7, ":num_volunteers", -1),
                                           ],
   "I can think of {reg5} whom I suspect would jump at the chance. If you could pay 10 denars {reg7?each for their equipment:for his equipment}.\
 Does that suit you?", "village_elder_recruit_decision", []],
]
