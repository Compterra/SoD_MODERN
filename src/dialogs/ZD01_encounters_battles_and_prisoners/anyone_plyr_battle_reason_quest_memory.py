DIALOGS = [
    [anyone, "plyr_battle_reason", [
        (store_conversation_troop, "$g_talk_troop"),
        (troop_slot_ge, "$g_talk_troop", slot_troop_sod_quest_memory_quest, 1),
        (call_script, "script_sod_quest_dialogue_read_memory", "$g_talk_troop"),
        (str_store_string_reg, s68, s4),
        (call_script, "script_sod_quest_dialogue_describe_battle_line", "$g_talk_troop"),
        (str_store_string_reg, s97, s68),
        (str_store_string, s68, "@{s97}^{s4}"),
    ],
    "{s68}", "plyr_battle_reason", []],
]
