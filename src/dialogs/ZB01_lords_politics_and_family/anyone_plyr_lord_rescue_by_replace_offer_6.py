DIALOGS = [
[anyone|plyr, "lord_rescue_by_replace_offer_6", [],
   "Quickly, {s65}, let us change garments. It is past time you were away from here.", "close_window",
   [(call_script, "script_succeed_quest", "qst_rescue_lord_by_replace"),
    (quest_get_slot, ":quest_target_troop", "qst_rescue_lord_by_replace", slot_quest_target_troop),
    (quest_get_slot, ":quest_target_center", "qst_rescue_lord_by_replace", slot_quest_target_center),
    (party_remove_prisoners, ":quest_target_center", ":quest_target_troop", 1),
    (troop_set_slot, ":quest_target_troop", slot_troop_prisoner_of_party, -1),
    (assign, "$auto_menu", -1),
    (assign, "$capturer_party", "$g_encountered_party"),
    (jump_to_menu, "mnu_captivity_rescue_lord_taken_prisoner"),
    (finish_mission),
    ]],
]
