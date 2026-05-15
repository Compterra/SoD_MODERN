DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_hero_freed),
                    (check_quest_active, "qst_kidnapped_girl"),
                    (neg|check_quest_concluded, "qst_kidnapped_girl"),
                    (store_conversation_troop, ":cur_troop"),
                    (eq, ":cur_troop", "trp_kidnapped_girl"), ],
   "Oh {sir/madam}. Thank you so much for rescuing me. Will you take me to my family now?", "kidnapped_girl_liberated_battle", []],
]
