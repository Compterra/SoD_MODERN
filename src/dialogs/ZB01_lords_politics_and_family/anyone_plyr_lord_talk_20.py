DIALOGS = [
[anyone|plyr, "lord_talk", [(le, "$talk_context", tc_party_encounter),
                             (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                             (eq, "$players_kingdom", "$g_talk_troop_faction"),
                             (eq, "$player_has_homage", 0),
                             (store_partner_quest, ":lords_quest"),
                             (neq, ":lords_quest", "qst_join_faction"),
                            ],
   "{s66}, take my oath and I will carry your banner into the field.", "lord_ask_enter_service", []],
]
