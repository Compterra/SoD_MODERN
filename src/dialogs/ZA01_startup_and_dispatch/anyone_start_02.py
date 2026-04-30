DIALOGS = [
    [anyone,
    "start",
    [
      (store_conversation_troop, "$g_talk_troop"),
      (is_between, "$g_talk_troop", companions_begin, companions_end),
      (eq, "$g_camp_talk", 1),
      (troop_slot_ge, "$g_talk_troop", slot_troop_sod_quest_memory_quest, 1),
      (call_script, "script_sod_quest_dialogue_read_memory", "$g_talk_troop"),
    ],
    "{s1}",
    "member_talk",
    [
      (call_script, "script_sod_quest_dialogue_describe_reaction", "$g_talk_troop"),
      (call_script, "script_sod_quest_dialogue_describe_stage", "$g_talk_troop")
    ]
  ],
]