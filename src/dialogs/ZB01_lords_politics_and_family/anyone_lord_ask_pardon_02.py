DIALOGS = [
[anyone, "lord_ask_pardon",
    [
      (store_sub, ":hostility", 4, "$g_talk_troop_faction_relation"),
      (val_mul, ":hostility", ":hostility"), #square it
      (store_mul, reg16, ":hostility", 10),
      #MORDACHAI - make their reaction a percentage modifier to the cost
      (assign, reg14, reg10),
      (assign, reg15, reg16),
      (val_mul, reg10, -1),   # invert sign
      (val_add, reg10, 100),  # convert to % multiplier (e.g. +20 = 80, -15 = 115)
      (val_mul, reg16, reg10), # multiply by the % modifier
      (val_div, reg16, 100),  # apply decimal place
      #(display_message, "@reaction was {reg14}, base cost = {reg15}, final cost = {reg16}", debug_color),
    ],
    "Hmm. I could use my considerable influence to arrange a pardon for you, {playername}, "\
    "but there are some who see you as an enemy and will not be satisfied unless you pay tribute."\
    "All in all, you'd need to bring no less than {reg16} denars to make any friends in {s4}.", "lord_ask_pardon_2", []],
]