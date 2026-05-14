DIALOGS = [
[anyone, "start", [
    (eq, "$talk_context", tc_party_encounter),
    (gt, "$g_encountered_party", 0),
    (party_is_active, "$g_encountered_party"),
    (gt, "$encountered_party_hostile", 0),
  ], "Surrender or die. Make your choice", "battle_reason_stated", []],
]
