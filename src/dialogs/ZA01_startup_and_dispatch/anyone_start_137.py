DIALOGS = [
[anyone , "start", [(store_conversation_troop, reg(1)),
                     (is_between, reg(1), arena_masters_begin, arena_masters_end),
                     (eq, "$arena_master_first_talk", 0),
                     ],
   "Good day friend. If you came to watch the tournaments you came in vain. There won't be a tournament here anytime soon.", "arena_intro_1", [(assign, "$arena_master_first_talk", 1)]],
]
