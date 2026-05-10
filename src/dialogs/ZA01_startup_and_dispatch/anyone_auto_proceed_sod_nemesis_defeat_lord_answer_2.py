DIALOGS = [
[anyone|auto_proceed, "defeat_lord_answer_2", [
    (eq, "$g_sod_nemesis_actor_type", sod_nemesis_actor_lord),
    (eq, "$g_sod_nemesis_last_troop", "$g_talk_troop"),
    (neq, "$g_talk_troop_faction", "fac_kingdom_6"),
    (troop_get_slot, reg21, "$g_talk_troop", slot_troop_sod_nemesis_mercy_count),
    (troop_get_slot, reg22, "$g_talk_troop", slot_troop_sod_nemesis_defeats),
  ],
  "none", "sod_nemesis_defeat_lord_released", []],
]
