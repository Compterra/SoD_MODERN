DIALOGS = [
[anyone, "lady_qst_duel_for_lady_failed_2", [], "It matters not, dear {playername}. You tried.\
 The truth cannot be proven at the point of a sword, but you willingly put your life at stake for my honour.\
 That alone will convince many of my innocence.", "lady_pretalk",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 6),
    (add_xp_as_reward, 400),
    (call_script, "script_end_quest", "qst_duel_for_lady"),
    ]],
]
