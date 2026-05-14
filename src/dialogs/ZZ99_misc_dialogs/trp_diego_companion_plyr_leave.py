DIALOGS = [
[trp_diego_companion|plyr, "diego_companion_talk",
  [
    (main_party_has_troop, "trp_diego_companion"),
    (eq, "$g_sod_diego_warning_pending", 4),
  ],
  "If you cannot follow this command any longer, go cleanly.",
  "diego_companion_departure",
  []],
[trp_diego_companion|plyr, "diego_companion_talk",
  [
    (main_party_has_troop, "trp_diego_companion"),
  ],
  "We should part ways for now.",
  "diego_companion_departure_confirm",
  []],
[trp_diego_companion|plyr, "diego_companion_talk", [],
  "That is all for now.", "close_window", []],
]
