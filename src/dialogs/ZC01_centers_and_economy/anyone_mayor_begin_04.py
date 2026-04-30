DIALOGS = [
[anyone, "mayor_begin", [(check_quest_active, "qst_move_cattle_herd"),
                          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_succeeded, "qst_move_cattle_herd"),
                          ],
   "Good to see you again {playername}. I have heard that you have delivered the cattle successfully.\
 I will tell the merchants how reliable you are.\
 And here is your pay, {reg8} denars.", "close_window",
   [(quest_get_slot, ":quest_gold_reward", "qst_move_cattle_herd", slot_quest_gold_reward),
    (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    (store_div, ":xp_reward", ":quest_gold_reward", 3),
    (add_xp_as_reward, ":xp_reward"),
    (call_script, "script_change_troop_renown", "trp_player", 1),
    (call_script, "script_change_player_relation_with_center", "$current_town", 3),
    (call_script, "script_end_quest", "qst_move_cattle_herd"),
    (assign, reg8, ":quest_gold_reward"),
    ]],
]
