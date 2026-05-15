DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc15"),
    (main_party_has_troop, "trp_npc15"),
    (eq, "$g_sod_artimenner_siege_pending", 1),
    (eq, "$g_sod_artimenner_siege_confronted", 1),
    (troop_slot_eq, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Artimenner, show me the weak point.", "companion_depth_artimenner_siege_pending",
  []],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc15"),
    (main_party_has_troop, "trp_npc15"),
  ],
  "Artimenner, are our plans still holding?", "companion_depth_artimenner",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc15"),
  ]],
]
