DIALOGS = [
[anyone|plyr, "deserter_talk", [
    (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
    (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
    (val_add, ":leadership", ":persuasion"),
    (ge, ":leadership", 6),
  ],
  "Lay down your arms. I can use soldiers who know when a battle is lost.",
  "deserter_recruit_offer",
  []],
]
