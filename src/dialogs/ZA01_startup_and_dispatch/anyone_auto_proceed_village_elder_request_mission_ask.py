DIALOGS = [
[anyone|auto_proceed, "village_elder_request_mission_ask", [], "A task?", "village_elder_tell_mission",
   [
       (call_script, "script_get_random_quest", "$g_talk_troop"),
       (assign, "$random_quest_no", reg0),
   ]],
]
