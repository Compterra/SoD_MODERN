DIALOGS = [
[anyone|plyr, "tavernkeeper_talk", [
      (store_current_hours, ":cur_hours"),
      (val_sub, ":cur_hours", 24),
      (gt, ":cur_hours", "$buy_drinks_last_time"),
      ], "I'd like to buy every man who comes in here tonight a jar of your best wine.", "tavernkeeper_buy_drinks", []],
]
