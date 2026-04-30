DIALOGS = [
[anyone, "player_siege_ask_surrender", [(lt, "$g_enemy_strength", 200), (store_mul, ":required_str", "$g_enemy_strength", 3), (ge, "$g_ally_strength", ":required_str")],
   "We are ready to leave this castle to you and march away if you give me your word of honour that you'll let us leave unmolested.", "player_siege_ask_leave_unmolested", []],
]
