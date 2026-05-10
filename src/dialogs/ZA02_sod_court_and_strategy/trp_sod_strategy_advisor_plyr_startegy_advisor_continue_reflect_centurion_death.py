DIALOGS = [
[trp_sod_strategy_advisor|plyr, "startegy_advisor_continue", [
    (troop_slot_eq, "trp_sod_strategy_advisor", slot_troop_sod_mentor_centurion_death, 1),
], "A Centurion is dead. What does that mean?", "sod_sa_reflect_centurion_death", [
    (troop_set_slot, "trp_sod_strategy_advisor", slot_troop_sod_mentor_centurion_death, 2),
]],
]
