DIALOGS = [
[trp_sod_strategy_advisor|plyr, "startegy_advisor_continue", [
    (faction_slot_eq, "fac_kingdom_6", slot_faction_state, sfs_defeated),
    (troop_slot_eq, "trp_sod_strategy_advisor", slot_troop_sod_mentor_final_closure, 0),
], "The Legion is broken. What lesson remains?", "sod_sa_reflect_final_closure", [
    (troop_set_slot, "trp_sod_strategy_advisor", slot_troop_sod_mentor_final_closure, 1),
]],
]
