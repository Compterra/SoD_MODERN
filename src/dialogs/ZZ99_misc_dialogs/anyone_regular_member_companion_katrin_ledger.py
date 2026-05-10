DIALOGS = [
[anyone, "regular_member_companion_katrin_ledger",
  [
    (try_begin),
      (eq, "$g_sod_katrin_last_coin_cause", 2),
      (str_store_string, s4, "@arrears, owed shares, and men folding promises like they were coin"),
    (else_try),
      (str_store_string, s4, "@thin sacks, thinner broth, and medicine cloth washed until it gives up"),
    (try_end),
  ],
  "Saying? Mostly counting. Katrin put {s4} in one column and asked whether courage can be boiled for supper. The camp wants the supply watch settled before the last coin becomes another speech.",
  "regular_member_talk",
  [
    (assign, "$g_sod_katrin_last_coin_witnessed", 1),
    (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_progress, 50),
    (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_metadata, "$g_sod_katrin_last_coin_result_grade"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_food_security, 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc11"),
    (display_message, "@A camp ledger witness brings Katrin's shortage into the company fires. The Last Coin in Camp now needs a supply watch, not another accounts entry.", 0x99CCFF),
  ]],
]
