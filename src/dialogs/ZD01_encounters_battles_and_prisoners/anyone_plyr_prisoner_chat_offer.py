DIALOGS = [
[anyone|plyr, "prisoner_chat_offer", [
                                      (neg|troop_is_hero, "$g_talk_troop"),
                                      (neq, "$g_talk_troop", "trp_khergit_chieftain"),
                                      ], "Swear to my company and you will be paid, fed, and armed. Refuse, and I sell your chain to the traders. Choose carefully.", "prisoner_chat_reaction",
                                      [(call_script, "script_determine_prisoner_agreed", "$g_talk_troop", "$g_talk_troop_relation")]],
]
