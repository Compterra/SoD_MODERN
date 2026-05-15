DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc2"),
    (main_party_has_troop, "trp_npc2"),
    (eq, "$g_sod_marnid_market_pending", 1),
    (troop_slot_eq, "trp_npc2", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Marnid, show me the suspect contract.", "companion_depth_marnid_price_pending",
  [
    (try_begin),
      (le, "$g_sod_marnid_market_focus_center", 0),
      (call_script, "script_sod_companion_start_marnid_market_incident", 1),
    (try_end),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc2"),
    (main_party_has_troop, "trp_npc2"),
  ],
  "Marnid, what do the accounts say about us?", "companion_depth_marnid",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc2"),
  ]],
]
