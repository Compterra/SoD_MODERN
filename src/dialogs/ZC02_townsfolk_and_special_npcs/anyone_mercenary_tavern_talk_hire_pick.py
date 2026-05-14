DIALOGS = [
[anyone, "mercenary_tavern_talk_hire_pick",
 [
   (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
   (party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
   (gt, ":mercenary_troop", 0),
   (gt, ":mercenary_amount", 0),
   (party_clear, "p_temp_party"),
   (party_add_members, "p_temp_party", ":mercenary_troop", ":mercenary_amount"),
   (assign, "$g_sod_tavern_merc_pick_start_amount", ":mercenary_amount"),
   (store_troop_gold, "$g_sod_tavern_merc_pick_gold_before", "trp_player"),
 ],
 "Choose who you want, then send the rest back to their cups.", "mercenary_tavern_talk_hire_pick_return",
 [
   (set_mercenary_source_party, "p_temp_party"),
   (change_screen_buy_mercenaries),
 ]],
]
