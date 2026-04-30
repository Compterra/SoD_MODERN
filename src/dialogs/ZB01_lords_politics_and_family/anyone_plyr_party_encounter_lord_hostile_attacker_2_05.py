DIALOGS = [
[anyone|plyr, "party_encounter_lord_hostile_attacker_2", [
                             (gt, "$supported_pretender", 0),
                             (eq, "$supported_pretender_old_faction", "$g_talk_troop_faction"),
                             (troop_slot_eq, "$g_talk_troop", slot_troop_discussed_rebellion, 0),
                             (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                             (troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1),
                             (call_script, "script_store_troop_name", s12, "$supported_pretender"),
                             (str_store_faction_name, s14, "$supported_pretender_old_faction"),
                             (faction_get_slot, ":old_faction_lord", "$supported_pretender_old_faction", slot_faction_leader),
                             (call_script, "script_store_troop_name", s15, ":old_faction_lord"),
                             ],
   "{s12} is your rightful ruler. Join our cause against the usurper, {s15}!", "lord_join_rebellion_suggest", []],
]
