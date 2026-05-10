DIALOGS = [
[anyone|plyr, "castle_patrol_talk", [
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (ge, ":renown", 350),
], "You know my banner. Do not make this costly.", "castle_patrol_threaten", []],
]
