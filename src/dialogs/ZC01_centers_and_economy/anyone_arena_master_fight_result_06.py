DIALOGS = [
[anyone , "arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (assign, reg8, "$g_arena_training_kills"),
     (assign, reg10, arena_tier4_prize),
     ],
   "That was damned good fighting, {playername}. You have very good moves, excellent tactics.\
 And you earned a prize of {reg10} denars for knocking down {reg8} opponents.", "arena_master_pre_talk",
   [
     (call_script, "script_troop_add_gold", "trp_player", arena_tier4_prize),
     (add_xp_to_troop, 10, "trp_player"),
     (assign, "$last_training_fight_town", -1),
     ]],
]
