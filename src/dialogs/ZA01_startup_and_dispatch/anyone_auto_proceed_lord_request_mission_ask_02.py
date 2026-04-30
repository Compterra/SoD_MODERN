DIALOGS = [
[anyone|auto_proceed, "lord_request_mission_ask", [], "A task?", "lord_tell_mission",
   [
       (call_script, "script_get_random_quest", "$g_talk_troop"),
       (assign, "$random_quest_no", reg0),
   ]],
]
