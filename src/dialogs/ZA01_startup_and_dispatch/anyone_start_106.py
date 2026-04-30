DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_hero_freed),
                    (store_conversation_troop, ":cur_troop"),
                    (eq, ":cur_troop", "trp_kidnapped_girl"), ],
   "Thank you for rescuing me {sir/madam}. Did the Serpent Host sent you", "sh_spy_liberated_battle", []],
]
