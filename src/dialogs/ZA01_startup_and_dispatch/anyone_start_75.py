DIALOGS = [
[anyone, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_seneschal), (eq, "$g_talk_troop_met", 0), (str_store_party_name, s68, "$g_encountered_party")],
   "Good day, {sir/madam}. I do not believe I've seen you here before.\
 Let me extend my welcome to you as the seneschal of {s68}.", "seneschal_intro_1", []],
]
