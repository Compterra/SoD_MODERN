DIALOGS = [
[anyone, "liege_defends_claim_3", [],
   "{s48}", "liege_defends_claim_4", [
                     (store_sub, ":rebellion_string", "$g_talk_troop_faction", "fac_kingdom_1"),
                     (val_add, ":rebellion_string", "str_swadian_rebellion_monarch_response_1"),
                     (str_store_string, 48, ":rebellion_string"),
                     ]],
]
