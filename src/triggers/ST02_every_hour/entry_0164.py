SIMPLE_TRIGGERS = [
(1, [
    # Defensive reset for legacy set_show_messages suppression leaks.
    (set_show_messages, 1),
    # Repair rare late-campaign party identity drift that can make hostile lords
    # and hired mercenaries appear neutral and stop reacting to the player.
    (call_script, "script_sod_campaign_party_sanity"),
  ]),
]
