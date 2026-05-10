DIALOGS = [
[anyone|plyr, "battle_reason_stated", [
    (party_get_num_prisoners, ":prisoners", "p_main_party"),
    (gt, ":prisoners", 0),
], "I have a prisoner worth more than my purse. Take them and let us pass.", "hostile_prisoner_exchange_offer", []],
]
