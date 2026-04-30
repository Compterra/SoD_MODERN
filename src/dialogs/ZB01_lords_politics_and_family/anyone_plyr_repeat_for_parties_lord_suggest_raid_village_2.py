DIALOGS = [
[anyone|plyr|repeat_for_parties, "lord_suggest_raid_village_2", [
                                                                       (store_repeat_object, ":center_no"),
                                                                       (party_slot_eq, ":center_no", slot_party_type, spt_village),
                                                                       (store_faction_of_party, ":town_faction", ":center_no"),
                                                                       (store_relation, ":town_relation", ":town_faction", "$g_talk_troop_faction"),
                                                                       (le, ":town_relation", -10),
                                                                       (str_store_faction_name, s2, ":town_faction"),
                                                                       (str_store_party_name, s1, ":center_no")],
   "{s1} of {s2}", "lord_suggest_raid_village_3", [(store_repeat_object, "$suggested_to_attack_center")]],
]
