DIALOGS = [
[trp_sod_chancellor, "start",
    [(troop_slot_eq, "trp_sod_chancellor", slot_troop_met_previously, 0)],
    "Your Highness, the seals and rolls are in order. I will keep the court's business ready: "\
    "oaths, fiefs, war papers, truces, colors, and the condition of the realm. "\
    "Give the word, and I will put the right parchment before you.",
    "chancellor_talk",
    [(troop_set_slot, "trp_sod_chancellor", slot_troop_met_previously, 1)]],
]
