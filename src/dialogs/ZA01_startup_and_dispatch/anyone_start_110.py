DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", ransom_brokers_begin, ransom_brokers_end),
                    (eq, "$g_talk_troop_met", 0)],
   "Greetings to you, {sir/madam}. You look like someone who should get to know me.", "ransom_broker_intro", []],
]
