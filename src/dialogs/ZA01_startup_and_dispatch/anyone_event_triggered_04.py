DIALOGS = [
[anyone, "event_triggered", [
                     (store_conversation_troop, "$map_talk_troop"),
                     (eq, "$map_talk_troop", "$npc_is_quitting"),
                     (is_between, "$map_talk_troop", companions_begin, companions_end),
                     (main_party_has_troop, "$map_talk_troop"),
                     (troop_get_slot, ":honorific", "$map_talk_troop", slot_troop_honorific),
                     (str_store_string, 5, ":honorific")],
   "{s5} -- there is something I need to tell you.", "companion_quitting", [
                    (assign, "$npc_is_quitting", 0),
                    (assign, "$player_can_persuade_npc", 1),
                    (assign, "$player_can_refuse_npc_quitting", 1),
       ]],
]
