DIALOGS = [
[anyone|plyr, "tavernkeeper_talk", [
      (store_current_hours, ":cur_hours"),
      (val_sub, ":cur_hours", 24),
      (gt, ":cur_hours", "$buy_drinks_last_time"),
      ], "I'd like to buy me and my men a barrel of your best ale.", "tavernkeeper_buy_drinks_troops", []],
]
