DIALOGS = [
[anyone , "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
                     (eq, "$g_talk_troop_met", 0),
                     (lt, "$g_talk_troop_faction_relation", 0),
                     (le, "$talk_context", tc_siege_commander),
                     ],
   "{s43}", "lord_meet_enemy", [
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_enemy_meet_default"),
       ]],
]
