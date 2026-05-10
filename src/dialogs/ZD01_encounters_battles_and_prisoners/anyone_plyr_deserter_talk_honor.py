DIALOGS = [
[anyone|plyr, "deserter_talk", [
    (ge, "$player_honor", 10),
    (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
    (ge, ":persuasion", 1),
], "You were soldiers once. Walk away with what honor you have left.", "deserter_honor_appeal", []],
]
