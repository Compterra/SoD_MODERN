DIALOGS = [
[anyone|plyr, "tavernkeeper_talk",
 [
   (gt, "$tavernkeeper_party", 0),
   (store_party_size, ":available", "$tavernkeeper_party"),
   (gt, ":available", 0),
 ],
 "I need local hands who can march today. Who is looking for pay?", "tavernkeeper_buy_peasants", []],
]
