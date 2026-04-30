DIALOGS = [
[anyone|plyr|repeat_for_100, "town_dweller_talk",
   [
     (store_repeat_object, ":object"),
     (lt, ":object", 4), # repeat only 4 times

     (check_quest_active, "qst_meet_spy_in_enemy_town"),
     (neg|check_quest_succeeded, "qst_meet_spy_in_enemy_town"),
     (quest_slot_eq, "qst_meet_spy_in_enemy_town", slot_quest_target_center, "$current_town"),

     (store_add, ":string", ":object", "str_secret_sign_1"),
     (str_store_string, s4, ":string"),
     ],
   "{s4}", "town_dweller_quest_meet_spy_in_enemy_town",
   [
     (store_repeat_object, ":object"),
     (assign, "$temp", ":object"),
     ]],
]
