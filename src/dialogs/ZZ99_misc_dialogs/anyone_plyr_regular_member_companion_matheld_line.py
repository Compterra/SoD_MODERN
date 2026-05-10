DIALOGS = [
[anyone|plyr, "regular_member_talk",
  [
    (main_party_has_troop, "trp_npc8"),
    (eq, "$g_sod_matheld_no_backward_step_pending", 1),
    (eq, "$g_sod_matheld_no_backward_step_witnessed", 0),
    (eq, "$g_sod_matheld_no_backward_step_confronted", 0),
    (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Matheld says the line learned something after that fight. What did you see?", "regular_member_companion_matheld_line", []],
]
