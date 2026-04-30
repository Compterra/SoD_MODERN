SCRIPTS = [
("finish_quest",
    [
      (store_script_param_1, ":quest_no"),
      (store_script_param_2, ":finish_percentage"),

      (quest_get_slot, ":quest_giver", ":quest_no", slot_quest_giver_troop),
      (quest_get_slot, ":quest_importance", ":quest_no", slot_quest_importance),
      (quest_get_slot, ":quest_xp_reward", ":quest_no", slot_quest_xp_reward),
      (quest_get_slot, ":quest_gold_reward", ":quest_no", slot_quest_gold_reward),

      (try_begin),
        (lt, ":finish_percentage", 100),
        (val_mul, ":quest_xp_reward", ":finish_percentage"),
        (val_div, ":quest_xp_reward", 100),
        (val_mul, ":quest_gold_reward", ":finish_percentage"),
        (val_div, ":quest_gold_reward", 100),
        #Changing the relation factor. Negative relation if less than 75% of the quest is finished.
        #Positive relation if more than 75% of the quest is finished.
        (assign, ":importance_multiplier", ":finish_percentage"),
        (val_sub, ":importance_multiplier", 75),
        (val_mul, ":quest_importance", ":importance_multiplier"),
        (val_div, ":quest_importance", 100),
      (else_try),
        (val_div, ":quest_importance", 4),
        (val_add, ":quest_importance", 1),
        (call_script, "script_change_player_relation_with_troop", ":quest_giver", ":quest_importance"),
      (try_end),

      (add_xp_as_reward, ":quest_xp_reward"),
      (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
      (call_script, "script_end_quest", ":quest_no"),
  ]),
]
