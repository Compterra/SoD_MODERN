DIALOGS = [
[anyone , "lord_persuade_lords_to_make_peace_pay", [],
   "Oh, yes, of course. We had already got the money for you.\
 Here, please accept these {reg12} denars together with our most sincere thanks.\
 If peace can keep the war from devouring the realm, then let it be done.", "close_window",
   [(quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
    (call_script, "script_troop_add_gold", "trp_player", ":quest_reward"),
    (call_script, "script_change_player_relation_with_center", "$current_town", 5),
    (call_script, "script_end_quest", "qst_persuade_lords_to_make_peace"),
    (quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
    (assign, reg12, ":quest_reward")
    ]],
]