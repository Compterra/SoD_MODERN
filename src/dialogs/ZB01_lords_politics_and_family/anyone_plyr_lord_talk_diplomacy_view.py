DIALOGS = [
[anyone|plyr, "lord_talk", [
    (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
    (is_between, "$g_talk_troop_faction", kingdoms_begin, kingdoms_end),
  ],
  "How fares your realm's politics?", "lord_diplomacy_view", [
    (call_script, "script_sod_diplomacy_describe_lord_view_to_s30", "$g_talk_troop"),
  ]],
]
