MENUS = [
(
    "collect_taxes_revolt_warning", 0,
    "The people of {s3} are outraged at your demands and decry it as nothing more than extortion. They're getting very restless, and they may react badly if you keep pressing them.",
    "none",
    [(str_store_party_name, s3, "$current_town"),
     ],
    [
      ("continue_collecting_taxes", [], "Ignore them and continue.",
       [(change_screen_return), ]),
      ("halve_taxes", [(quest_get_slot, ":quest_giver_troop", "qst_collect_taxes", slot_quest_giver_troop),
                       (call_script, "script_store_troop_name", s1, ":quest_giver_troop"), ],
       "Agree to reduce your collection by half. ({s1} may be upset)",
       [(assign, "$qst_collect_taxes_halve_taxes", 1),
        (change_screen_return),
        ]),
    ]
  ),
]
