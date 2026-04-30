DIALOGS = [
[anyone , "arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (lt, "$g_arena_training_kills", arena_tier2_opponents_to_beat),
     (assign, reg8, "$g_arena_training_kills"),
     (assign, reg10, arena_tier1_prize),
     ],
   "You put up quite a good fight there. Good moves. You definitely show promise.\
 And you earned a prize of {reg10} denars for knocking down {reg8} opponents.", "arena_master_pre_talk", [
     (call_script, "script_troop_add_gold", "trp_player", arena_tier1_prize),
     (add_xp_to_troop, 5, "trp_player"),
     (assign, "$last_training_fight_town", -1)]],
]
