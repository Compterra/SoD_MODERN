DIALOGS = [
[anyone, "event_triggered", [
                     (eq, "$npc_map_talk_context", slot_troop_personalitymatch_state),
                     (store_conversation_troop, "$map_talk_troop"),
                     (eq, "$map_talk_troop", "$npc_with_personality_match"),
                     (main_party_has_troop, "$map_talk_troop"),

                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalitymatch_speech),
                     (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalitymatch_object),
                     (main_party_has_troop, ":object"),
                     (call_script, "script_store_troop_name", 11, ":object"),
                     (str_store_string, 5, ":speech"),
                     ],
   "{s5}", "companion_personalitymatch_b", [
                    (assign, "$npc_with_personality_match", 0),
       ]],
]
