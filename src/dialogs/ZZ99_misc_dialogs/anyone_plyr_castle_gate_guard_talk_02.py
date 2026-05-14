DIALOGS = [
[anyone|plyr, "castle_gate_guard_talk", [
  (party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
  (is_between, ":castle_lord", 0, "trp_last_troop"),
], "Tell your lord I am at the gate and asking for audience.", "request_meeting_castle_lord", []],
]
