DIALOGS = [
[anyone, "member_castellan_join", [(party_can_join_party, "$g_encountered_party", "p_main_party")],
   "I've grown quite fond of the place... But if it is your wish, {playername}, I'll come with you.", "close_window", [
       (assign, "$g_move_heroes", 1),
       (call_script, "script_party_add_party", "p_main_party", "$g_encountered_party"),
       (party_clear, "$g_encountered_party"),
       ]],
]
