MENUS = [
("jc_change_bet", 0,
    "How much do you want to bet?",
    "none",
    [
    ],
    [
      (
        "bet_1", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 100) ],
        "100 denars.",
        [
          (assign, "$g_jotnar_clan_competition_bet", 100),(jump_to_menu, "$g_next_menu"),
        ]
      ),
      (
        "bet_2", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 50) ],
        "50 denars.",
        [
          (assign, "$g_jotnar_clan_competition_bet", 50),(jump_to_menu, "$g_next_menu"),
        ]
      ),
      (
        "bet_3", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 20) ],
        "20 denars.",
        [
          (assign, "$g_jotnar_clan_competition_bet", 20),(jump_to_menu, "$g_next_menu"),
        ]
      ),
      (
        "bet_4", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 10) ],
        "10 denars.",
        [
          (assign, "$g_jotnar_clan_competition_bet", 10),(jump_to_menu, "$g_next_menu"),
        ]
      ),
      (
        "bet_5", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 5) ],
        "5 denars.",
        [
          (assign, "$g_jotnar_clan_competition_bet", 5),(jump_to_menu, "$g_next_menu"),
        ]
      ),
	  (
        "bet_6", [],
        "No bet.",
        [
          (assign, "$g_jotnar_clan_competition_bet", 0),(jump_to_menu, "$g_next_menu"),
        ]
      ),
    ]
  ),
]
