DIALOGS = [
[trp_sod_strategy_advisor, "event_triggered", [
  (eq, "$sa_talk_after_siege", 1),
  (main_party_has_troop, "trp_sod_strategy_advisor"),
  ], "A little blood in the throat, my liege. The old wound is making its argument again.", "sod_sa_after_1", [(assign, "$sa_talk_after_siege", 0)]],
]
