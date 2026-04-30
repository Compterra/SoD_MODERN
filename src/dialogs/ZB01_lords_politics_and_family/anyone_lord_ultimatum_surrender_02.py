DIALOGS = [
[anyone, "lord_ultimatum_surrender", [], "{s43}", "lord_attack_verify_b", #originally, you will not survive this
   [
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_unnecessary_attack_default"),
    (call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -5),
    ]],
]
