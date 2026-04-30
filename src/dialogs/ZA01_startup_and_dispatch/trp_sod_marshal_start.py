DIALOGS = [
[trp_sod_marshal, "start", [(troop_slot_eq, "trp_sod_marshal", slot_troop_met_previously, 0)],
    "Greetings Your Royal Highness. Thank You for appointing me for as the Marshall. I will serve you as with utter diligence and care.  "\
    "Whenever You want to discuss military matters such as upgrading troops or preparing military campaigns just talk to me.", "marshal_talk",
    [(troop_set_slot, "trp_sod_marshal", slot_troop_met_previously, 1), ]],
]
