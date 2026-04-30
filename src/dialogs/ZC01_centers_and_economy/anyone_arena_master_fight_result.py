DIALOGS = [
[anyone , "arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (eq, "$g_arena_training_kills", 0)
     ],
   "Ha-ha, that's quite the bruise you're sporting. But don't worry; everybody gets trounced once in awhile. The important thing is to pick yourself up, dust yourself off and keep fighting. That's what champions do.", "arena_master_pre_talk", [(assign, "$last_training_fight_town", -1)]],
]
