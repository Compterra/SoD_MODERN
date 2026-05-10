DIALOGS = [
[anyone|plyr, "prisoner_chat_offer", [
                                      (neg|troop_is_hero, "$g_talk_troop"),
                                      (neq, "$g_talk_troop", "trp_khergit_chieftain"),
                                      ], "You have one last chance to redeem yourself before I sell you to the slave-traders.  "\
                                      "Drop all your previous allegiances and swear fealty to me, obey my every order to the letter, and you'll be paid, fed and equipped.  "\
                                      "If you don't....well, let's just say that life as a slave will be seemingly unending years of agony, malnutrition and beatings.  "\
                                      "I'd advise you to think very, very carefully before choosing.", "prisoner_chat_reaction",
                                      [(call_script, "script_determine_prisoner_agreed", "$g_talk_troop", "$g_talk_troop_relation")]],
]
