DIALOGS = [
[anyone, "town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         (assign, ":walker_type", reg0),
                                         (eq, ":walker_type", walkert_needs_money),
                                         (party_slot_eq, "$current_town", slot_party_type, spt_village)],
   "Disaster has struck my family, {sir/madam}. A pestilence has ruined the crops on our fields, and my poor children lie at home hungry and sick.\
 My neighbours are too poor themselves to help me.", "town_dweller_poor", []],
[anyone, "town_dweller_ask_situation", [(party_slot_eq, "$current_town", slot_party_type, spt_village),
                                         (party_slot_eq, "$current_town", slot_village_state, svs_recovering)],
   "We are putting the village back together, {sir/madam}. The fields are sown again, but every shout in the night still makes folk reach for the door bar.", "town_dweller_talk", []],
]
