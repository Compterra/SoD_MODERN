DIALOGS = [
[anyone, "merchant_quest_persuade_peace_4", [], "They are {s12} from {s15} and {s13} from {s14}. Until they change their mind or lose their influence,\
 there will be no chance of having peace between the two sides.", "merchant_quest_persuade_peace_5", [
       (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
       (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
       (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
       (call_script, "script_store_troop_name_link", s12, ":quest_object_troop"),
       (call_script, "script_store_troop_name_link", s13, ":quest_target_troop"),
       (str_store_faction_name_link, s14, ":quest_target_faction"),
       (str_store_faction_name_link, s15, "$g_encountered_party_faction"),
     ]],
]
