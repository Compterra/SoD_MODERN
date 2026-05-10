DIALOGS = [
[trp_sod_strategy_advisor|plyr, "startegy_advisor_continue", [
    (troop_slot_eq, "trp_sod_strategy_advisor", slot_troop_sod_mentor_first_imperial_victory, 1),
], "What did our first victory over the Legion teach you?", "sod_sa_reflect_imperial_victory", [
    (troop_set_slot, "trp_sod_strategy_advisor", slot_troop_sod_mentor_first_imperial_victory, 2),
]],
]
