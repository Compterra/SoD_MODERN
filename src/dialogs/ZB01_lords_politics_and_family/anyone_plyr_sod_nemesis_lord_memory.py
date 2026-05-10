DIALOGS = [
[anyone|plyr, "lord_talk", [
    (eq, "$g_sod_nemesis_actor_type", sod_nemesis_actor_lord),
    (ge, "$g_sod_nemesis_state", sod_nemesis_state_watching),
    (eq, "$g_sod_nemesis_last_troop", "$g_talk_troop"),
    (neq, "$g_talk_troop_faction", "fac_kingdom_6"),
  ],
  "You remember me more than most lords do.", "sod_nemesis_lord_memory", []],
]
