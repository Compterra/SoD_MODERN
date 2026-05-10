DIALOGS = [
[trp_sod_strategy_advisor, "event_triggered", [
  (this_or_next|main_party_has_troop, "trp_sod_strategy_advisor"),
  (eq, "$g_sod_sa_in_court", 1),
  (call_script, "script_get_random_string_for_troop", s1, "$g_talk_troop"),
  ], "{s1}", "startegy_advisor_continue", []],
]
