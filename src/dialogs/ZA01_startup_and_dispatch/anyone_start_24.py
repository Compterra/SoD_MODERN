DIALOGS = [
[anyone, "start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_black_army_aid_warband"),
                         (check_quest_succeeded, "qst_black_army_aid_warband"),
                         ],
   "Brilliant work, princeling!", "gm_pretalk",
   [
    (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 5),
    (call_script, "script_troop_add_gold", "trp_player", 500),
    (add_xp_as_reward, 800),
    (call_script, "script_succeed_quest", "qst_black_army_aid_warband"),
    (call_script, "script_end_quest", "qst_black_army_aid_warband")
    ]],
]
