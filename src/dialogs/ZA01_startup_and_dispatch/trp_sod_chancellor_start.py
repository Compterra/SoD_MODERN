DIALOGS = [
[trp_sod_chancellor, "start",
    [(troop_slot_eq, "trp_sod_chancellor", slot_troop_met_previously, 0)],
    "Greetings Your Highness. Thank You for appointing me for as your Chancellor. "\
    "I will serve and be available for you whenever needed. "\
    "Whenever You want to discuss matters such as managing Your fiefs, recruiting Lords, "\
    "declaring war or other kingdom management matters just call me.",
    "chancellor_talk",
    [(troop_set_slot, "trp_sod_chancellor", slot_troop_met_previously, 1)]],
]
