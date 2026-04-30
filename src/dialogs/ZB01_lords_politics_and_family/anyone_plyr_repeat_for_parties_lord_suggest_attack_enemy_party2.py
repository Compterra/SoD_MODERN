DIALOGS = [
[anyone|plyr|repeat_for_parties, "lord_suggest_attack_enemy_party2", [
                                                                       (store_repeat_object, ":party_no"),
                                                                       (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
                                                                       (party_is_active, ":party_no"),
                                                                       (store_faction_of_party, ":party_faction", ":party_no"),
                                                                       (store_relation, ":party_relation", ":party_faction", "$g_talk_troop_faction"),
                                                                       (le, ":party_relation", -10),
                                                                       (call_script, "script_get_closest_walled_center", ":party_no"),
                                                                       (assign, ":center_no", reg0),
                                                                       (str_store_party_name, s3, ":center_no"),
                                                                       (str_store_faction_name, s2, ":party_faction"),
                                                                       (str_store_party_name, s1, ":party_no")],
   "{s1} of {s2} around {s3}", "lord_suggest_attack_enemy_party3", [(store_repeat_object, "$suggested_to_attack_party")]],
]
