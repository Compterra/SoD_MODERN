DIALOGS = [
[anyone, "start", [(this_or_next|is_between, "$g_talk_troop", weapon_merchants_begin, weapon_merchants_end),
                    (this_or_next|is_between, "$g_talk_troop", armor_merchants_begin, armor_merchants_end),
                    (             is_between, "$g_talk_troop", horse_merchants_begin, horse_merchants_end)], "Good day. Steel, leather, and horseflesh all have their moods; tell me what kind of trouble you are preparing for.", "town_merchant_talk", []],
]
