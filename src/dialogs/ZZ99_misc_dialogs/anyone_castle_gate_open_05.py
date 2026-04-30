DIALOGS = [
[anyone, "castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                               (call_script, "script_store_troop_name", s2, ":castle_lord"),
  ],  "My lord {s2} does not want you here. Begone now.", "close_window", []],
]
