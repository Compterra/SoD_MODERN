DIALOGS = [
[anyone, "tavernkeeper_buy_drinks", [],
   "Of course, {my lord/my lady}. I reckon {reg5} denars should be enough for that. What should I tell the lads?", "tavernkeeper_buy_drinks_2", [
    (assign, "$temp", 1000),
    (assign, reg5, "$temp"),
  ]],
]
