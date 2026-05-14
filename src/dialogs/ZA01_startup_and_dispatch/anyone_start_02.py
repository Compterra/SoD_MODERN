DIALOGS = [
    [anyone,
    "start",
    [
      (store_conversation_troop, "$g_talk_troop"),
      (is_between, "$g_talk_troop", companions_begin, companions_end),
      (eq, "$g_camp_talk", 1),
    ],
    "Yes?",
    "member_talk",
    []
  ],
]
