DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc1"),
    (main_party_has_troop, "trp_npc1"),
    (eq, "$g_sod_borcha_road_pending", 1),
    (troop_slot_eq, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Borcha, show me the road before it chooses us.", "companion_depth_borcha_road_pending",
  [
    (try_begin),
      (le, "$g_sod_borcha_road_origin_center", 0),
      (call_script, "script_sod_companion_start_borcha_road_incident", 1),
    (try_end),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc1"),
    (main_party_has_troop, "trp_npc1"),
  ],
  "Borcha, tell me what the road is saying.", "companion_depth_borcha",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc1"),
  ]],
]
