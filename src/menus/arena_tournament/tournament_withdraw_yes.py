MENUS = [
(
    "tournament_withdraw_verify", 0,
    "Are you sure you want to withdraw from the tournament?",
    "none",
    [],
    [
      ("tournament_withdraw_yes", [], "Yes. This is a pointless affectation.",
       [(jump_to_menu, "mnu_town_tournament_won_by_another"),
        ]),
      ("tournament_withdraw_no", [], "No, not as long as there is a chance of victory!",
       [(jump_to_menu, "mnu_town_tournament"),
        ]),
    ]
  ),
]
