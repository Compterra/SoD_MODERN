DIALOGS = [
[anyone, "lord_collect_debt_pay", [],
   "I must admit I'm impressed, {playername}. I had lost hope of ever getting this money back. Please accept my sincere thanks.", "lord_pretalk", [
     (call_script, "script_sod_player_charge_gold", reg4),
     (play_sound, "snd_money_paid"),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
     (add_xp_as_reward, 100),
     (call_script, "script_end_quest", "qst_collect_debt")
     ]],
]
