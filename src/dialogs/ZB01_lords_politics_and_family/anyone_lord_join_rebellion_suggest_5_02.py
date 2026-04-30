DIALOGS = [
[anyone, "lord_join_rebellion_suggest_5", [
            (encountered_party_is_attacker),
      ], "{s43}", "party_encounter_lord_hostile_attacker_2",
   [
        (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_rebellion_refuse_default"),

    ]],
]
