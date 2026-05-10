DIALOGS = [
[anyone , "member_chat", [
     (is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
     (eq, "$g_talk_troop", "$supported_pretender"),
     ],
   "Greetings, {playername}, my first and foremost vassal. I await your counsel.", "supported_pretender_talk", []],
]
