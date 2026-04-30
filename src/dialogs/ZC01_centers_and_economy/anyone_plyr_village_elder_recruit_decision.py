DIALOGS = [
[anyone|plyr, "village_elder_recruit_decision", [(party_slot_eq, "$current_town", slot_center_volunteer_troop_amount, 0)],
   "So be it.", "village_elder_pretalk", [(party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1), ]],
]
