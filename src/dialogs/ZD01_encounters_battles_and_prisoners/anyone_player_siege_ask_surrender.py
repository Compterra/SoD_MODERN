DIALOGS = [
[anyone, "player_siege_ask_surrender", [(lt, "$g_enemy_strength", 100), (store_mul, ":required_str", "$g_enemy_strength", 5), (ge, "$g_ally_strength", ":required_str")],
   "Perhaps... Do you give your word of honour that we'll be treated well?", "player_siege_ask_surrender_treatment", []],
]
