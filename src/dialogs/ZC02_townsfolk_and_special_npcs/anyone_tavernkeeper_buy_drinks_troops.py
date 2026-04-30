DIALOGS = [
[anyone, "tavernkeeper_buy_drinks_troops",
   [
    ], "Of course, {my lord/my lady}. I reckon {reg5} denars should be enough for that. What should I tell the lads?", "tavernkeeper_buy_drinks_troops_2", [
        (assign, "$temp", 20),
      (party_get_num_companions, reg5, "p_main_party"),
      (store_mul, "$temp", "$temp", reg5),
        (assign, reg5, "$temp"),
        ]],
]
