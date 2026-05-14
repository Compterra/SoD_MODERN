DIALOGS = [
[anyone|plyr, "ransom_broker_talk",
  [
    (neg|main_party_has_troop, "trp_diego_companion"),
    (troop_slot_eq, "trp_diego_companion", slot_troop_playerparty_history, pp_history_dismissed),
  ],
  "I need word carried to Diego, the one-eyed man from the Slaver pits.",
  "ransom_broker_find_diego",
  []],
]
