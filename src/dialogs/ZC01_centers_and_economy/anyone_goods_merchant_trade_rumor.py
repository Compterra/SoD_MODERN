DIALOGS = [
[anyone, "goods_merchant_trade_rumor", [
    (assign, ":health", 50),
    (try_begin),
      (is_between, "$current_town", centers_begin, centers_end),
      (party_get_slot, ":health", "$current_town", slot_center_sod_local_health),
    (try_end),
    (str_store_string, s24, "@The market is open enough, for now."),
    (try_begin),
      (lt, ":health", 15),
      (str_store_string, s24, "@Mind the sickness talk. Some merchants are keeping distance from stores they would have touched last season."),
    (else_try),
      (ge, ":health", 55),
      (str_store_string, s24, "@The town is healthier than most, and clean markets make bolder merchants."),
    (try_end),
  ],
   "Ask the caravans, captain. They know which roads are bleeding. From here I hear this market spoken of as a {s23}, and the drivers will tell you what that means in coin. {s24}", "goods_merchant_talk", []],
]
