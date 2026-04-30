DIALOGS = [
[anyone , "start", [(store_conversation_troop, reg(1)), (is_between, reg(1), arena_masters_begin, arena_masters_end)],
   "Hello {playername}. Good to see you again.", "arena_master_pre_talk", [(assign, "$arena_reward_asked", 0)]],
]
