DIALOGS = [
[anyone, "request_meeting_6",
   [
     (call_script, "script_troop_get_player_relation", "$lord_requested_to_talk_to"),
     (assign, ":lord_relation", reg0),
     (gt, ":lord_relation", -20),
    ], "All right. {s2} will talk to you now.", "close_window", [(call_script, "script_store_troop_name", s2, "$lord_requested_to_talk_to")]],
]
