DIALOGS = [
[anyone|auto_proceed , "start", [(store_conversation_troop, reg(1)), (is_between, reg(1), arena_masters_begin, arena_masters_end),
                     (eq, "$last_training_fight_town", "$current_town"),
                     (store_current_hours, ":cur_hours"),
                     (val_add, ":cur_hours", -4),
                     (lt, ":cur_hours", "$training_fight_time")],
   ".", "arena_master_fight_result", [(assign, "$arena_reward_asked", 0)]],
]
