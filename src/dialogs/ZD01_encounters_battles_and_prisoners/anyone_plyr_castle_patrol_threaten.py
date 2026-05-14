DIALOGS = [
[anyone|plyr, "castle_patrol_talk", [
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (ge, ":renown", 350),
], "My banner is not contraband. Search me with steel and answer for the cost.", "castle_patrol_threaten", []],
]
