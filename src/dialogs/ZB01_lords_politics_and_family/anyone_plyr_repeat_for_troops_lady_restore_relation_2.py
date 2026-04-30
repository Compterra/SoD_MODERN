DIALOGS = [
[anyone|plyr|repeat_for_troops, "lady_restore_relation_2", [(store_repeat_object, ":troop_no"),
                                                             (is_between, ":troop_no", heroes_begin, heroes_end),
                                                             (store_troop_faction, ":faction_no", ":troop_no"),
                                                             (eq, "$g_talk_troop_faction", ":faction_no"),
                                                             (call_script, "script_troop_get_player_relation", ":troop_no"),
                                                             (lt, reg0, 0),
                                                             (call_script, "script_store_troop_name", s1, ":troop_no")],
   "{s1}", "lady_restore_relation_2b", [(store_repeat_object, "$troop_to_restore_relations_with")]],
]
