DIALOGS = [
[anyone|plyr, "castle_patrol_talk", [
    (store_faction_of_party, ":patrol_faction", "$g_encountered_party"),
    (store_relation, ":relation", ":patrol_faction", "fac_player_faction"),
    (lt, ":relation", 0),
], "I demand passage. Stand aside.", "castle_patrol_demand_passage", []],
]
