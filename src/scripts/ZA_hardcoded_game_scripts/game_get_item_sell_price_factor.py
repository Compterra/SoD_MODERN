SCRIPTS = [
("game_get_item_sell_price_factor",
    [
      (store_script_param_1, ":item_kind_id"),
      (assign, ":price_factor", 100),

      (call_script, "script_get_trade_penalty", ":item_kind_id"),
      (assign, ":trade_penalty", reg0),

      (try_begin),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":price_factor", "$g_encountered_party", ":item_slot_no"),
        (val_mul, ":price_factor", 100), #normalize price factor to range 0..100
        (val_div, ":price_factor", average_price_factor),
      (else_try),
        #increase trade penalty while selling
        (val_mul, ":trade_penalty", 4),
      (try_end),


      (store_add, ":penalty_divisor", 100, ":trade_penalty"),

      (val_mul, ":price_factor", 100),
      (val_div, ":price_factor", ":penalty_divisor"),

      (assign, reg0, ":price_factor"),
      (set_trigger_result, reg0),
  ]),
]
