DIALOGS = [
[anyone, "seneschal_ask_about_someone_3", [(call_script, "script_troop_write_family_relations_to_s1", "$hero_requested_to_learn_relations"),
                                           (call_script, "script_troop_write_owned_centers_to_s2", "$hero_requested_to_learn_relations")],
   "{s2}{s1}", "seneschal_ask_about_someone_4", [(add_troop_note_from_dialog, "$hero_requested_to_learn_relations", 2)]],
]
