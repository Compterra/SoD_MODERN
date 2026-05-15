DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_hero_freed),
                    (check_quest_active, "qst_serpent_host_free_spy"),
                    (neg|check_quest_concluded, "qst_serpent_host_free_spy"),
                    (store_conversation_troop, ":cur_troop"),
                    (eq, ":cur_troop", "trp_sh_spy"), ],
   "Thank you for rescuing me, {sir/madam}. Did the Serpent Host send you?", "sh_spy_liberated_battle", []],
]
