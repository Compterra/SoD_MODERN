DIALOGS = [
[anyone, "start",
    [
      (gt, "$g_encountered_party", 0),
      (party_is_active, "$g_encountered_party"),
      (store_faction_of_party, ":cur_faction", "$g_encountered_party"),
      (eq, ":cur_faction", "fac_player_faction"),
      (this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_player_mercenaries),
      (party_slot_eq, "$g_encountered_party", slot_party_type, spt_player_patrol),
      (call_script, "script_sod_external_party_describe_status_to_s20", "$g_encountered_party"),
    ],
    "{s20}", "mate_chat_talk", [(assign, "$g_leave_encounter", 1)]],
]
