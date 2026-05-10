DIALOGS = [
[anyone|plyr, "regular_member_talk",
  [
    (main_party_has_troop, "trp_npc10"),
    (eq, "$g_sod_bunduk_line_pending", 1),
    (eq, "$g_sod_bunduk_line_witnessed", 0),
    (eq, "$g_sod_bunduk_line_confronted", 0),
    (troop_slot_eq, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Bunduk says the line has a grievance. Speak plainly.", "regular_member_companion_bunduk_line", []],
]
