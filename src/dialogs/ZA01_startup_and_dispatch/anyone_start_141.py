DIALOGS = [
[anyone, "start", [(party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
                    (this_or_next|is_between, "$g_talk_troop", weapon_merchants_begin, weapon_merchants_end),
                    (this_or_next|is_between, "$g_talk_troop", armor_merchants_begin, armor_merchants_end),
                    (             is_between, "$g_talk_troop", horse_merchants_begin, horse_merchants_end),
                    ],
   "Greetings, {your lordship/my lady}. How can I serve you today?", "town_merchant_talk", []],
]
