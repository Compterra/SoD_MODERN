DIALOGS = [
[anyone|plyr, "bandit_talk", [
    (store_skill_level, ":tracking", "skl_tracking", "trp_player"),
    (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
    (val_add, ":tracking", ":persuasion"),
    (ge, ":tracking", 3),
], "Tell me where your bands gather, and I may leave you enough road to run.", "bandit_hideout_clue_demand", []],
]
