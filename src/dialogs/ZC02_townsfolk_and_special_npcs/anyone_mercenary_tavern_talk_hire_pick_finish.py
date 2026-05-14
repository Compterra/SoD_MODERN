DIALOGS = [
[anyone, "mercenary_tavern_talk_hire_pick_finish",
 [
   (party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
   (gt, ":mercenary_amount", 0),
   (assign, reg6, ":mercenary_amount"),
 ],
 "{reg6} of us will stay in town a while longer, if your purse or your plans change.", "close_window",
 [
   (party_clear, "p_temp_party"),
   (assign, "$g_sod_tavern_merc_pick_start_amount", 0),
   (assign, "$g_sod_tavern_merc_pick_gold_before", 0),
 ]],

[anyone, "mercenary_tavern_talk_hire_pick_finish", [],
 "Then the bargain is struck. Keep the pay fair and the road bloody enough, and we will serve.", "close_window",
 [
   (party_clear, "p_temp_party"),
   (assign, "$g_sod_tavern_merc_pick_start_amount", 0),
   (assign, "$g_sod_tavern_merc_pick_gold_before", 0),
 ]],
]
