DIALOGS = [
[anyone|plyr|repeat_for_troops, "lord_talk_ask_location_2",
    [(store_repeat_object, ":troop_no"),
     (neq, "$g_talk_troop", ":troop_no"),
     (is_between, ":troop_no", heroes_begin, heroes_end),
     (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
     (store_troop_faction, ":faction_no", ":troop_no"),
     (eq, "$g_encountered_party_faction", ":faction_no"),
     (call_script, "script_store_troop_name", s1, ":troop_no")
    ],
    "{s1}", "lord_talk_ask_location_3", [(store_repeat_object, "$hero_requested_to_learn_location")]],
]
