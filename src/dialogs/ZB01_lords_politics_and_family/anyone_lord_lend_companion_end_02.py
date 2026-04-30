DIALOGS = [
[anyone, "lord_lend_companion_end", [],
   "Certainly, {playername}. {reg3?She:He} is a bright {reg3?girl:fellow}, you're a lucky {man/woman} to have such worthy companions.", "lord_pretalk",
   [(quest_get_slot, ":quest_target_troop", "qst_lend_companion", slot_quest_target_troop),
    (party_add_members, "p_main_party", ":quest_target_troop", 1),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
    (add_xp_as_reward, 100),
    (call_script, "script_end_quest", "qst_lend_companion"),
    (call_script, "script_store_troop_name", s14, ":quest_target_troop"),
    (troop_get_type, reg3, ":quest_target_troop"),
    ]],
]
