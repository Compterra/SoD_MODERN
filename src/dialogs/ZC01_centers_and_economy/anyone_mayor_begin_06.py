DIALOGS = [
[anyone, "mayor_begin", [(check_quest_active, "qst_kidnapped_girl"),
                          (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 4),
                          (quest_slot_eq, "qst_kidnapped_girl", slot_quest_giver_troop, "$g_talk_troop"),
                          ],
   "Dear {playername}. I am in your debt for bringing back my friend's daughter.\
  Please take these {reg8} denars that I promised you.\
  My friend wished he could give more but paying that ransom brought him to his knees.", "close_window",
   [(quest_get_slot, ":quest_gold_reward", "qst_kidnapped_girl", slot_quest_gold_reward),
    (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    (assign, reg8, ":quest_gold_reward"),
    (assign, ":xp_reward", ":quest_gold_reward"),
    (val_mul, ":xp_reward", 2),
    (val_add, ":xp_reward", 100),
    (add_xp_as_reward, ":xp_reward"),
    (call_script, "script_change_troop_renown", "trp_player", 3),
    (call_script, "script_change_player_relation_with_center", "$current_town", 2),
    (call_script, "script_end_quest", "qst_kidnapped_girl"),
    ]],
]
