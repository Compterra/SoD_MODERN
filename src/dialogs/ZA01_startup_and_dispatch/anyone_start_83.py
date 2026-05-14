DIALOGS = [
[anyone, "start", [(gt, "$g_encountered_party", 0), (party_is_active, "$g_encountered_party"), (party_slot_eq, "$g_encountered_party", slot_party_type, spt_kingdom_caravan), (this_or_next|eq, "$talk_context", tc_party_encounter), (eq, "$talk_context", 0)],
   "Hail, traveler. Our wheels are warm and the ledgers are open; ask quickly if you want road news or trade.", "merchant_talk", []],
]
