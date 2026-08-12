DIALOGS = [
[anyone, "event_triggered", [
                     (eq, "$npc_map_talk_context", slot_troop_home),
                     (store_conversation_troop, "$map_talk_troop"),
                     (is_between, "$map_talk_troop", companions_begin, companions_end),
                     (main_party_has_troop, "$map_talk_troop"),
                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_home_intro),
                     (str_store_string, s5, ":speech"),
                     ],
   "{s5}", "companion_home_description", [
                    (troop_set_slot, "$map_talk_troop", slot_troop_home_speech_delivered, 1),
       ]],
]
