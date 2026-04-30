DIALOGS = [
[anyone, "caravan_offer_protection_6", [(get_party_ai_object, ":caravan_destination", "$g_encountered_party"),
    (str_store_party_name, 1, ":caravan_destination")],
   "Good. Come and collect your money when we're within sight of {s1}. For now, let's just get underway.", "close_window",
   [(get_party_ai_object, ":caravan_destination", "$g_encountered_party"),
    (assign, "$caravan_escort_destination_town", ":caravan_destination"),
    (assign, "$caravan_escort_party_id", "$g_encountered_party"),
    (assign, "$caravan_escort_agreed_reward", "$caravan_escort_offer"),
    (assign, "$caravan_escort_state", 1),
    (assign, "$g_leave_encounter", 1)
   ]],
]
