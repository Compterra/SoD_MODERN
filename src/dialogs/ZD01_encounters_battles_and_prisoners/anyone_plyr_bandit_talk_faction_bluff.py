DIALOGS = [
[anyone|plyr, "bandit_talk", [
    (gt, "$players_kingdom", 0),
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (ge, ":renown", 120),
], "My banner is not prey. It is jurisdiction. Clear the road.", "hostile_faction_bluff", []],
]
