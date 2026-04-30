DIALOGS = [
[anyone, "merchant_quest_requested", [(eq, "$random_merchant_quest_no", "qst_persuade_lords_to_make_peace"),
                                       (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
                                       (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
                                       (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
                                       (call_script, "script_store_troop_name_link", s12, ":quest_object_troop"),
                                       (call_script, "script_store_troop_name_link", s13, ":quest_target_troop"),
                                       (str_store_faction_name_link, s14, ":quest_target_faction"),
                                       (str_store_faction_name_link, s15, "$g_encountered_party_faction"), ],
   "This war between {s15} and {s14} has brought our town to the verge of ruin.\
 Our caravans get raided before they can reach their destination.\
 Our merchants are afraid to leave the safety of the town walls.\
 And as if those aren't enough, the taxes to maintain the war take away the last bits of our savings.\
 If peace does not come soon, we can not hold on for much longer.", "merchant_quest_persuade_peace_1",
   []],
]
