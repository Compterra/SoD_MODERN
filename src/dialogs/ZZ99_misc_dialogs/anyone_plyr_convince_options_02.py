DIALOGS = [
[anyone|plyr, "convince_options",
  [(store_div, "$convince_relation_penalty", "$convince_value", 300),
   (val_add, "$convince_relation_penalty", 1),
   (assign, reg9, "$convince_relation_penalty")],
   "Please, do it for the sake of our friendship. (-{reg9} to relation)", "convince_friendship", []],
]
