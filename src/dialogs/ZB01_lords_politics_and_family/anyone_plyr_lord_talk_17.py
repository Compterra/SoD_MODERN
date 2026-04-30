DIALOGS = [
[anyone|plyr, "lord_talk", [(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                             (eq, "$players_kingdom", "$g_talk_troop_faction"),
                             (eq, "$player_has_homage", 0),
                             (gt, "$mercenary_service_accumulated_pay", 0),
                             ],
   "{s67}, I humbly request the weekly payment for my service.", "lord_pay_mercenary", []],
]
