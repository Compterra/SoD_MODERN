MENUS = [
(
    "invite_player_to_faction_accepted", 0,
    "In order to become a vassal, you must swear an oath of homage to {s3}. You shall have to find him and give him your oath in person. {s5}",
    "none",
    [
        (call_script, "script_get_information_about_troops_position", "$g_invite_faction_lord", 0),
        (call_script, "script_store_troop_name", s3, "$g_invite_faction_lord"),
        (str_store_string, s5, "@{s1}"),
      ],
    [
      ("continue", [], "Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
]
