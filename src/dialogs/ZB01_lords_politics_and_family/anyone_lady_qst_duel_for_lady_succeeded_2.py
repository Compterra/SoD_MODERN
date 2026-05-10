DIALOGS = [
[anyone, "lady_qst_duel_for_lady_succeeded_2", [], "{s10}", "lady_pretalk",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 10),
    (add_xp_as_reward, 1000),
    (call_script, "script_troop_add_gold", "trp_player", 2000),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_tournament_glory, 3),
    (call_script, "script_end_quest", "qst_duel_for_lady"),
    ]],
]
