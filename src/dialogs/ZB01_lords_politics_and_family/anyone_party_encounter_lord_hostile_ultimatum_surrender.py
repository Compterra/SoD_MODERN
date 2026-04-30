DIALOGS = [
[anyone, "party_encounter_lord_hostile_ultimatum_surrender", [],
   "{s43}", "close_window", [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_challenged_default"),
       (call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),
       (try_begin),
         (gt, "$g_talk_troop_relation", -10),
         (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
       (try_end),
       (assign, "$encountered_party_hostile", 1)]],
]
