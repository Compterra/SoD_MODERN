DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_kill_local_merchant"),
                         (check_quest_succeeded, "qst_kill_local_merchant"),
                         (quest_slot_eq, "qst_kill_local_merchant", slot_quest_current_state, 1)],
   "I heard you got rid of that poxy merchant that was causing me so much grief.\
 I can see you're not afraid to get your hands dirty, eh? I like that in a {man/woman}.\
 Here's your reward. Remember, {playername}, stick with me and we'll go a long, long way together.", "close_window",
   [ (call_script, "script_troop_add_gold", "trp_player", 600),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 4),
     (add_xp_as_reward, 300),
     (call_script, "script_end_quest", "qst_kill_local_merchant"),

     (call_script, "script_objectionable_action", tmt_humanitarian, "str_murder_merchant"),

     (assign, "$g_leave_encounter", 1)]],
]
