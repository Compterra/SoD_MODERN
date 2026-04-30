DIALOGS = [
[anyone|plyr, "town_dweller_talk",
   [
     (eq, 1, 0),
     (check_quest_active, "qst_meet_spy_in_enemy_town"),
     (neg|check_quest_succeeded, "qst_meet_spy_in_enemy_town"),
     (quest_slot_eq, "qst_meet_spy_in_enemy_town", slot_quest_target_center, "$current_town"),
     (str_store_item_name, s5, "$spy_item_worn"),
     ],
   "Pardon me, but is that a {s5} you're wearing?", "town_dweller_quest_meet_spy_in_enemy_town_ask_item",
   [
     ]],
]
