DIALOGS = [
[anyone, "request_meeting_castle_lord", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
                                         (eq, "$g_encountered_party", reg0),
                                         (call_script, "script_store_troop_name", s2, ":castle_lord"),
                                         (assign, "$lord_requested_to_talk_to", ":castle_lord"),
                                          ],  "Wait here. {s2} will see you.", "close_window", [
                                            (call_script, "script_setup_troop_meeting", "$lord_requested_to_talk_to", 0),
                                          ]],
]
