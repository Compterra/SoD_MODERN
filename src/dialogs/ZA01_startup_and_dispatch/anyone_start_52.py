DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_hero_defeated),
                    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero)],
   "{s43}", "defeat_lord_answer",
   [(troop_set_slot, "$g_talk_troop", slot_troop_leaded_party, -1),
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_surrender_offer_default"),
    ]],
]
