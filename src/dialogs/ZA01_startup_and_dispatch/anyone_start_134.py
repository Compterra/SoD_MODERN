DIALOGS = [
[anyone , "start", [(is_between, "$g_talk_troop", goods_merchants_begin, goods_merchants_end),
                     (party_slot_eq, "$current_town", slot_town_lord, "trp_player")],
   "{My lord/my lady}, my shop is humble, but every sack and bolt in it answers to the roads you keep. How may I serve?", "goods_merchant_talk", []],
]
