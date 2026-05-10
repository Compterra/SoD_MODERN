DIALOGS = [
[anyone|plyr, "bandit_talk", [
    (store_num_parties_destroyed_by_player, ":looters_destroyed", "pt_bandits"),
    (store_num_parties_destroyed_by_player, ":mountain_destroyed", "pt_mountain_bandits"),
    (store_num_parties_destroyed_by_player, ":forest_destroyed", "pt_forest_bandits"),
    (val_add, ":looters_destroyed", ":mountain_destroyed"),
    (val_add, ":looters_destroyed", ":forest_destroyed"),
    (ge, ":looters_destroyed", 8),
], "I have put enough outlaws in the ground to make a road of bones. Move.", "bandit_outlaw_slayer_reaction", []],
]
