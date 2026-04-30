DIALOGS = [
[anyone , "arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (lt, "$g_arena_training_kills", arena_tier3_opponents_to_beat),
     (assign, reg8, "$g_arena_training_kills"),
     (assign, reg10, arena_tier2_prize),
     (assign, reg12, arena_tier2_opponents_to_beat),
     ],
   "That was a good fight you put up there. You managed to take down no less than {reg8} opponents.\
 And of course, you earned a prize money of {reg10} denars.", "arena_master_pre_talk", [
     (call_script, "script_troop_add_gold", "trp_player", arena_tier2_prize),
     (add_xp_to_troop, 10, "trp_player"),
     (assign, "$last_training_fight_town", -1)]],
]
