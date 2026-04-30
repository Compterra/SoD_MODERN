DIALOGS = [
[anyone , "start", [(store_conversation_troop, reg(1)),
                     (is_between, reg(1), arena_masters_begin, arena_masters_end),
                     (assign, "$arena_reward_asked", 0), #set some variables.
                     (assign, "$arena_tournaments_asked", 0),
                     (eq, 1, 0),
                     ],
   ".", "arena_intro_1", []],
]
