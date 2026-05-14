DIALOGS = [
[anyone|plyr, "lord_talk",
   [
     (eq, "$g_talk_troop_faction", "$players_kingdom"),
     (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
     (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
     (faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_default),
     ],
   "Send the summons. The army gathers here, and the campaign begins.", "lord_give_order_call_to_arms_verify",
   []],
]
