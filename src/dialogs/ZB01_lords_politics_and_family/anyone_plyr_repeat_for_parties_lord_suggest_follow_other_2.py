DIALOGS = [
[anyone|plyr|repeat_for_parties, "lord_suggest_follow_other_2", [
                                                                       (store_repeat_object, ":party_no"),
                                                                       (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
                                                                       (neq, ":party_no", "$g_talk_troop"),
                                                                       (store_faction_of_party, ":party_faction", ":party_no"),
                                                                       (eq, ":party_faction", "$g_talk_troop_faction"),
                                                                       (str_store_party_name, s1, ":party_no")],
   "{s1}", "lord_suggest_follow_other_3", [(store_repeat_object, "$town_suggested_to_go_to")]],
]
