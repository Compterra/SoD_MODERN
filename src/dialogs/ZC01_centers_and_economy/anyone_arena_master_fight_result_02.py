DIALOGS = [
[anyone , "arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (lt, "$g_arena_training_kills", arena_tier1_opponents_to_beat),
     (assign, reg8, "$g_arena_training_kills")
     ],
   "Hey, you managed to take down {reg8} opponents. Not bad. But that won't bring you any prize money.\
 Now, if I were you, I would go back there and show everyone what I can do...", "arena_master_pre_talk", [(assign, "$last_training_fight_town", -1)]],
]
