DIALOGS = [
[trp_sod_strategy_advisor|plyr, "startegy_advisor_continue", [
    (troop_slot_eq, "trp_sod_strategy_advisor", slot_troop_sod_mentor_alliance_victory, 1),
], "Did the coalition matter in that Imperial victory?", "sod_sa_reflect_alliance_victory", [
    (troop_set_slot, "trp_sod_strategy_advisor", slot_troop_sod_mentor_alliance_victory, 2),
]],
]
