DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
    (troop_slot_eq, "$g_talk_troop", slot_troop_companion_warning_state, sod_companion_warning_pending),
  ],
  "You have a grievance. Speak plainly.", "companion_warning_direct",
  []],

[anyone|plyr, "member_talk",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
    (this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_companion_warning_state, sod_companion_warning_final),
    (troop_slot_eq, "$g_talk_troop", slot_troop_companion_warning_state, sod_companion_warning_acknowledged),
    (troop_get_slot, ":approval", "$g_talk_troop", slot_troop_companion_approval),
    (lt, ":approval", 45),
  ],
  "We need to mend this.", "companion_reconciliation_direct",
  []],
]
