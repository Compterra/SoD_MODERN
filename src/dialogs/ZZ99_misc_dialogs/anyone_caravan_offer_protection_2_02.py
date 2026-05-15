DIALOGS = [
[anyone, "caravan_offer_protection_2", [(get_party_ai_object, ":caravan_destination", "$g_encountered_party"),
    (str_store_party_name, s68, ":caravan_destination"),
    (assign, reg(2), "$caravan_escort_offer")],
   "We are heading to {s68}. I will pay you {reg2} denars if you escort us there.", "caravan_offer_protection_3",
   []],
]
