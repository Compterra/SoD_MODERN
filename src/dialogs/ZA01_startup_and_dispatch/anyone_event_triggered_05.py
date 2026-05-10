DIALOGS = [
[anyone, "event_triggered", [
                     (store_conversation_troop, "$map_talk_troop"),
                     (eq, "$map_talk_troop", "$npc_with_grievance"),
                     (main_party_has_troop, "$map_talk_troop"),
                     (eq, "$npc_map_talk_context", slot_troop_morality_state),

                     (try_begin),
                         (eq, "$npc_grievance_slot", slot_troop_morality_state),
                         (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_morality_speech),
                     (else_try),
                         (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_2ary_morality_speech),
                     (try_end),
                     (str_store_string, 21, "$npc_grievance_string"),
                     (str_store_string, 5, ":speech"),
                     ],
   "{s5}", "companion_objection_response", [
                    (assign, "$npc_with_grievance", 0),
       ]],
]
