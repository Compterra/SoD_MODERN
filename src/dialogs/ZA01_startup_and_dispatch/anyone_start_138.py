DIALOGS = [
[anyone , "start", [(store_conversation_troop, reg(1)),
                     (is_between, reg(1), arena_masters_begin, arena_masters_end),
                     (eq, "$g_talk_troop_met", 0),
                     ],
   "Hello. You seem to be new here. Care to share your name?", "arena_master_intro_1", []],
]
