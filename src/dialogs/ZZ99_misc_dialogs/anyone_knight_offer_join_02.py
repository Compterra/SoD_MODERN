DIALOGS = [
[anyone , "knight_offer_join", [(lt, "$g_talk_troop_relation", 5),
                                 (store_character_level, ":player_level", "trp_player"),
                                 (store_character_level, ":talk_troop_level", "$g_talk_troop"),
                                 (val_mul, ":player_level", 2),
                                 (lt, ":player_level", ":talk_troop_level")],
   "You forget your place, {sir/madam}. I do not take orders from the likes of you.", "hero_pretalk", []],
]
