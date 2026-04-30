SIMPLE_TRIGGERS = [
(1,
   [
      (ge, "$g_player_raiding_village", 1),
      (try_begin),
        (neq, "$g_player_is_captive", 0),
        (rest_for_hours, 0, 0, 0), #stop resting - abort
        (assign, "$g_player_raiding_village", 0),
      (else_try),
        (map_free), #we have been attacked during raid
        (assign, "$g_player_raiding_village", 0),
      (else_try),
        (this_or_next|party_slot_eq, "$g_player_raiding_village", slot_village_state, svs_looted),
        (party_slot_eq, "$g_player_raiding_village", slot_village_state, svs_deserted),
        (start_encounter, "$g_player_raiding_village"),
        (rest_for_hours, 0),
        (assign, "$g_player_raiding_village", 0),
        (assign, "$g_player_raid_complete", 1),
      (else_try),
        (party_slot_eq, "$g_player_raiding_village", slot_village_state, svs_being_raided),
        (rest_for_hours, 3, 5, 1), #rest while attackable
      (else_try),
        (rest_for_hours, 0, 0, 0), #stop resting - abort
        (assign, "$g_player_raiding_village", 0),
        (assign, "$g_player_raid_complete", 0),
      (try_end),
    ]),
]
