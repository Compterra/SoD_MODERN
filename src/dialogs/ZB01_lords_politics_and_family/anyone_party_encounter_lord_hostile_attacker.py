DIALOGS = [
[anyone, "party_encounter_lord_hostile_attacker", [
      (gt, "$g_comment_found", 0),
                    ],
   "{s42}", "party_encounter_lord_hostile_attacker", [
                         (try_begin),
                           (neq, "$log_comment_relation_change", 0),
                           (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", "$log_comment_relation_change"),
                         (try_end),
                         (assign, "$g_comment_found", 0),
                    ]],
]
