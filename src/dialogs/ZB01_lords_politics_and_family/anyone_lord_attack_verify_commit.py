DIALOGS = [
[anyone, "lord_attack_verify_commit", [], "{s43}", "close_window",
   [
	(assign, "$g_enemy_party", "$g_encountered_party"),
	(call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_challenged_default"),
    (call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -30),
    (encounter_attack),
    ]],
]
