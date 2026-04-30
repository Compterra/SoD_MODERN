DIALOGS = [
[anyone|plyr|repeat_for_parties, "lord_suggest_go_to_friendly_town2", [
                                                                       (store_repeat_object, ":center_no"),
                                                                       (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_castle),
                                                                       (party_slot_eq, ":center_no", slot_party_type, spt_town),
                                                                       (neq, ":center_no", "$g_encountered_party"),
                                                                       (store_faction_of_party, ":town_faction", ":center_no"),
                                                                       (eq, ":town_faction", "$g_talk_troop_faction"),
                                                                       (str_store_party_name, s1, ":center_no")],
   "{s1}", "lord_suggest_go_to_friendly_town3", [(store_repeat_object, "$town_suggested_to_go_to")]],
]
