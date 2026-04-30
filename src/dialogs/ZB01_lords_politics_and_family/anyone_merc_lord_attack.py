DIALOGS = [
[anyone, "merc_lord_attack", [
   (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", -40),
   (call_script, "script_update_all_notes"),
   ],
   "As you wish. Defend yourself.", "close_window", [],],
]
