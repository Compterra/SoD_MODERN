MENUS = [
(
    "tournament_bet_confirm", 0,
    "If you bet {reg1} denars, you will earn {reg2} denars if you win the tournament. Is that all right?",
    "none",
    [
      (call_script, "script_get_win_amount_for_tournament_bet"),
      (assign, ":win_amount", reg0),
      (val_mul, ":win_amount", "$temp"),
      (val_div, ":win_amount", 100),
      (assign, reg1, "$temp"),
      (assign, reg2, ":win_amount"),
      ],
    [
      ("tournament_bet_accept", [],
       "Go ahead.",
       [
         (call_script, "script_tournament_place_bet", "$temp"),
         (jump_to_menu, "mnu_town_tournament"),
         ]),
      ("tournament_bet_cancel", [],
       "Forget it.",
       [
         (jump_to_menu, "mnu_tournament_bet"),
         ]),
    ]
  ),
]
