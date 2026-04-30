DIALOGS = [
[anyone , "arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (lt, "$g_arena_training_kills", arena_tier4_opponents_to_beat),
     (assign, reg8, "$g_arena_training_kills"),
     (assign, reg10, arena_tier3_prize)
     ],
   "Your performance was amazing! You are without doubt a very skilled fighter.\
 Not everyone can knock down {reg8} people in the fights. Of course you deserve a prize with that performance: {reg10} denars. Nice, eh?", "arena_master_pre_talk", [
     (call_script, "script_troop_add_gold", "trp_player", arena_tier3_prize),
     (add_xp_to_troop, 10, "trp_player"),
     (assign, "$last_training_fight_town", -1)]],
]
