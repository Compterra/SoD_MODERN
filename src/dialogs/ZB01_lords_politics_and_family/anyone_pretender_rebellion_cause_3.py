DIALOGS = [
[anyone, "pretender_rebellion_cause_3", [],
   "{s48}", "pretender_start", [
                     (troop_get_slot, ":rebellion_string", "$g_talk_troop", slot_troop_original_faction),
                     (val_sub, ":rebellion_string", "fac_kingdom_1"),
                     (val_add, ":rebellion_string", "str_swadian_rebellion_pretender_story_3"),
                     (str_store_string, 48, ":rebellion_string"),
                     ]],
]
