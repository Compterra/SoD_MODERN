DIALOGS = [
    [anyone, "plyr_battle_reason", [
        (store_conversation_troop, "$g_talk_troop"),
        (call_script, "script_sod_quest_dialogue_read_memory", "$g_talk_troop"),
    ],
    "{s1}", "plyr_battle_reason", [
        (call_script, "script_sod_quest_dialogue_describe_battle_line", "$g_talk_troop"),
    ]],
]