DIALOGS = [
[anyone, "prison_guard_visit_prison", [(this_or_next|faction_slot_eq, "$g_encountered_party_faction", slot_faction_marshall, "trp_player"),
                                        (this_or_next|party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
                                        (eq, "$g_encountered_party_faction", "$players_kingdom"),
                                        ],
   "Of course, {sir/madam}. Go in.", "close_window", [(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],
]
