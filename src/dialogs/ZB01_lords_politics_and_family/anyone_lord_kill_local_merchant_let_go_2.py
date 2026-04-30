DIALOGS = [
[anyone, "lord_kill_local_merchant_let_go_2", [],
   "Piffle. You were supposed to remove him, not give him a sermon and send him on his way.\
 He had better do as you say, or you'll both regret it.\
 Here, this is half the money I promised you. Don't say a word, {playername}, you're lucky to get even that.\
 I have little use for {men/people} who cannot follow orders.", "lord_pretalk",
   [(call_script, "script_troop_add_gold", "trp_player", 300),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
     (add_xp_as_reward, 500),
     (call_script, "script_end_quest", "qst_kill_local_merchant"),
     (assign, "$g_leave_encounter", 1)
    ]],
]
