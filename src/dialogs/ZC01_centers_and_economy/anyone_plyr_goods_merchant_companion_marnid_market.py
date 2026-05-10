DIALOGS = [
[anyone|plyr, "goods_merchant_talk",
  [
    (main_party_has_troop, "trp_npc2"),
    (call_script, "script_cf_sod_companion_campaign_available", "trp_npc2", sod_companion_campaign_mode_dialog),
    (eq, "$g_sod_marnid_market_pending", 1),
    (eq, "$g_sod_marnid_market_contacted", 0),
    (eq, "$current_town", "$g_sod_marnid_market_focus_center"),
    (troop_slot_eq, "trp_npc2", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Marnid wants a merchant's plain account of fair dealing in this market.", "goods_merchant_companion_marnid_market",
  [
    (call_script, "script_sod_trade_network_describe_center_identity_to_s23", "$current_town"),
  ]],
]
