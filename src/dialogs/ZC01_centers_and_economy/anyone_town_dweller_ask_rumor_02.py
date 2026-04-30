DIALOGS = [
[anyone, "town_dweller_ask_rumor", [(store_mul, ":rumor_id", "$current_town", 197),
                                     (val_add,  ":rumor_id", "$g_talk_agent"),
                                     (call_script, "script_get_rumor_to_s61", ":rumor_id"),
                                     (gt, reg0, 0)], "{s61}", "town_dweller_talk", []],
]
