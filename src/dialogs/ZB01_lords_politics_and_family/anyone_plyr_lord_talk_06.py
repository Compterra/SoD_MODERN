DIALOGS = [
[anyone|plyr, "lord_talk", [(check_quest_active, "qst_persuade_lords_to_make_peace"),
                            (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
                            (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
                            (this_or_next|eq, ":quest_target_troop", "$g_talk_troop"),
                            (eq, ":quest_object_troop", "$g_talk_troop"),
                            (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
                            (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
                            (str_store_faction_name, s12, ":quest_target_faction"),
                            (str_store_faction_name, s13, ":quest_object_faction"),
                            ],
   "Please, {s64}, it's time to end this war between {s12} and {s13}.", "lord_ask_to_make_peace",
   [(assign, "$g_convince_quest", "qst_persuade_lords_to_make_peace")]],
]
