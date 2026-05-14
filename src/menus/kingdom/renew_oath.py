MENUS = [
(
    "oath_fulfilled", 0,
  "Your term of mercenary service with {s1} has expired. What will you do?",
    "none",
    [
      (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
      (call_script, "script_store_troop_name", s1, ":faction_leader"),
    ],
    [
      ("renew_oath",
        [(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
         (call_script, "script_store_troop_name", s1, ":faction_leader")],
        "Renew your kingdom service with {s1} for another month.",
        [(store_current_day, ":cur_day"),
         (store_add, "$mercenary_service_next_renew_day", ":cur_day", 30),
         (change_screen_return), ]),

      ("dont_renew_oath", [], "Become free of your bond.",
       [(call_script, "script_player_leave_faction", 1),
        (change_screen_return), ]),
    ]
  ),
]
