SIMPLE_TRIGGERS = [
(7,
    [
      # Campaign AI cadence: every 7 hours. Keep this trigger as a thin
      # dispatch layer; safety checks live in the called scripts and static
      # modernization coverage.
      (call_script, "script_init_ai_calculation"),
      (call_script, "script_decide_kingdom_party_ais"),
      ]),
]
