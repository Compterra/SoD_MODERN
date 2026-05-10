DIALOGS = [
[anyone|plyr, "sod_prisoner_train_talk", [
    (party_slot_ge, "$g_encountered_party", slot_party_sod_prisoner_military_count, 1),
  ], "I can help arrange ransom or exchange for the military captives.", "close_window", [
    (call_script, "script_sod_player_negotiate_prisoner_train_ransom_exchange", "$g_encountered_party"),
    (assign, reg5, reg0),
    (try_begin),
      (gt, reg5, 0),
      (display_message, "@Your negotiation processed {reg5} military captives through ransom and exchange channels.", 0x99CCFF),
    (else_try),
      (display_message, "@The guards refuse the terms or you lack the broker fee.", 0xCC9966),
    (try_end),
    (assign, "$g_leave_encounter", 1),
  ]],
]
