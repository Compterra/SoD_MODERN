DIALOGS = [
    [anyone, "lord_start", [
        (store_conversation_troop, "$g_talk_troop"),
        (is_between, "$g_talk_troop", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_slot_ge, "$g_talk_troop", slot_troop_sod_quest_memory_quest, 1),
        (call_script, "script_sod_quest_dialogue_read_memory", "$g_talk_troop"),
        (str_store_string_reg, s68, s4),
        (call_script, "script_sod_quest_dialogue_describe_reaction", "$g_talk_troop"),
        (str_store_string_reg, s97, s68),
        (str_store_string, s68, "@{s97}^{s4}"),
        (call_script, "script_sod_quest_dialogue_describe_stage", "$g_talk_troop"),
        (str_store_string_reg, s97, s68),
        (str_store_string, s68, "@{s97}^{s4}"),
    ],
    "{s68}", "lord_start", []],
]
