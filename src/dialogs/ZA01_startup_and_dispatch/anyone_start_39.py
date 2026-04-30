DIALOGS = [
[anyone, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_player_companion),
                    (neg|main_party_has_troop, "$g_talk_troop"),
                    (eq, "$talk_context", tc_party_encounter)],
   "Do you want me to rejoin you?", "member_wilderness_talk", []],
]
