DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (eq, "$talk_context", tc_tavern_talk),
                     (main_party_has_troop, "$g_talk_troop")],
   "Let's leave whenever you are ready.", "close_window", []],
]
