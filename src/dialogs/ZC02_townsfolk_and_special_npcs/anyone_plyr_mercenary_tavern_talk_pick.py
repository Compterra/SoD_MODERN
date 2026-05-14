DIALOGS = [
[anyone|plyr, "mercenary_tavern_talk",
 [
   (party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
   (gt, ":mercenary_amount", 1),
 ],
 "Line them up. I want to choose the blades I hire.", "mercenary_tavern_talk_hire_pick", []],
]
