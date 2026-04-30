DIALOGS = [
[anyone , "start",
   [
     (is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
     (eq, "$g_talk_troop", "$supported_pretender"),
     ],
   "I await your counsel, {playername}.", "supported_pretender_talk", [
     ]],
]
