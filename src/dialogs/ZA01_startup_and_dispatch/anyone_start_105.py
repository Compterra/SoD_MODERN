DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_hero_freed),
                    (store_conversation_troop, ":cur_troop"),
                    (eq, ":cur_troop", "trp_kidnapped_girl"), ],
   "Oh {sir/madam}. Thank you so much for rescuing me. Will you take me to my family now?", "kidnapped_girl_liberated_battle", []],
]
