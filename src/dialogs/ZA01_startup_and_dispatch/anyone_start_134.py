DIALOGS = [
[anyone , "start", [(is_between, "$g_talk_troop", goods_merchants_begin, goods_merchants_end),
                     (party_slot_eq, "$current_town", slot_town_lord, "trp_player")],
   "{My lord/my lady}, you honour my humble shop with your presence.", "goods_merchant_talk", []],
]
