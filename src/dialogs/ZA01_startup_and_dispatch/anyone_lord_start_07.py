DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_meet_spy_in_enemy_town"),
                         (check_quest_succeeded, "qst_meet_spy_in_enemy_town"),
                         ],
   "Have you brought me any news about that task I gave you? You know the one I mean...", "quest_meet_spy_in_enemy_town_completed",
   []],
]
