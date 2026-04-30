MENUS = [
(
    "village_loot_continue", 0,
    "Do you wish to continue looting this village?",
    "none",
    [],
    [
      ("disembark_yes", [], "Yes.",
        [(rest_for_hours, 3, 5, 1), #rest while attackable (3 hours will be extended by the trigger)
         (change_screen_return), ]),

      ("disembark_no", [], "No.",
        [(call_script, "script_village_set_state", "$current_town", 0),
         (party_set_slot, "$current_town", slot_village_raided_by, -1),
         (assign, "$g_player_raiding_village", 0),
         (change_screen_return)]),
    ],
  ),
]
