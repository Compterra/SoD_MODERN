DIALOGS = [
[anyone|plyr|repeat_for_parties, "lord_suggets_attack_enemy_castle2", [
                                                                       (store_repeat_object, ":center_no"),
                                                                       (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_castle),
                                                                       (party_slot_eq, ":center_no", slot_party_type, spt_town),
                                                                       (store_faction_of_party, ":town_faction", ":center_no"),
                                                                       (store_relation, ":town_relation", ":town_faction", "$g_talk_troop_faction"),
                                                                       (le, ":town_relation", -10),
                                                                       (str_store_faction_name, s2, ":town_faction"),
                                                                       (str_store_party_name, s1, ":center_no")],
   "{s1} of {s2}", "lord_suggets_attack_enemy_castle3", [(store_repeat_object, "$suggested_to_attack_center")]],
]
