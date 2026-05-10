DIALOGS = [
[anyone, "goods_merchant_companion_marnid_market", [],
  "Then he should hear this plainly: a {s23} does not stay useful if every bargain leaves one side desperate. The contract you are asking after has clean ink and dirty names. Look behind the warehouse before the broker rewrites the debt again.",
  "goods_merchant_talk",
  [
    (assign, "$g_sod_marnid_market_contacted", 1),
    (assign, "$g_sod_marnid_market_evidence", 1),
    (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_progress, 50),
    (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_last_center, "$current_town"),
    (call_script, "script_sod_companion_shift_core_value_proof", "trp_npc2", 1),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_orderly_profit, 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc2"),
    (display_message, "@A market contact gives Marnid's Honest Price a public witness and a warehouse lead.", 0x99CCFF),
  ]],
]
