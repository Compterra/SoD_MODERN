DIALOGS = [
[anyone|plyr, "castle_patrol_talk", [
    (store_faction_of_party, ":patrol_faction", "$g_encountered_party"),
    (store_relation, ":relation", ":patrol_faction", "fac_player_faction"),
    (lt, ":relation", 0),
], "I claim passage under my banner. Do not turn patrol duty into insult.", "castle_patrol_demand_passage", []],
]
