DIALOGS = [
[anyone, "loa_rejected", [], "I see.  I shall seek my fortunes elsewhere.", "close_window",
    [
      # rejected - record the outcome
      (troop_set_slot, "$g_talk_troop", slot_lord_allegience_offered, lao_rejected),
      (store_random_in_range, reg0, -30, 0),
      (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", reg0),
      (assign, "$g_sod_lord_offers_allegience", 0)
    ]
  ],
]
