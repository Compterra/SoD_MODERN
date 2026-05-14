DIALOGS = [
[anyone, "lord_ask_leave_service_3", [], "Then let every witness here understand the break.\
 Your oath to my house is ended, your duties are released, and no title of mine shelters you from what follows.\
 Walk free, {playername}, but do not pretend freedom leaves no footprints.", "lord_ask_leave_service_end",
   [
        (call_script, "script_add_log_entry", logent_renounced_allegiance,   "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction"),
        (call_script, "script_player_leave_faction", 1),
    ]],
]
