MENUS = [
(
    "village_loot_no_resist", 0,
    "The villagers here are few and frightened, and they quickly scatter and run before you. The village is at your mercy.",
    "none",
    [],
    [
      ("village_loot", [], "Plunder the village, then raze it.",
       [
          (store_faction_of_party, ":center_faction", "$current_town"),
          (call_script, "script_sod_diplomacy_record_event", ":center_faction", sod_diplomacy_memory_border_raid, 1),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_abuse_village, 5),
          (call_script, "script_village_set_state", "$current_town", svs_being_raided),
          (party_set_slot, "$current_town", slot_village_raided_by, "p_main_party"),
          (assign, "$g_player_raiding_village", "$current_town"),
          (rest_for_hours, 3, 5, 1), #rest while attackable (3 hours will be extended by the trigger)
          (change_screen_return),
           ]),
      ("village_raid_leave", [], "Leave this village alone.", [(change_screen_return)]),
    ],
  ),
]
