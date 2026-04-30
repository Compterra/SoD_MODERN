SCRIPTS = [
("center_change_trade_good_production",
    [
      (store_script_param, ":center_no", 1),
      (store_script_param, ":item_no", 2),
      (store_script_param, ":production_rate", 3),
      #      (val_mul, ":production_rate", 5),
      (store_script_param, ":randomness", 4),
      (store_random_in_range, ":random_num", 0, ":randomness"),
      (store_random_in_range, ":random_sign", 0, 2),
      (try_begin),
        (eq, ":random_sign", 0),
        (val_add, ":production_rate", ":random_num"),
      (else_try),
        (val_sub, ":production_rate", ":random_num"),
      (try_end),
      (val_sub, ":item_no", trade_goods_begin),
      (val_add, ":item_no", slot_town_trade_good_productions_begin),

      (party_get_slot, ":old_production_rate", ":center_no", ":item_no"),
      (val_add, ":production_rate", ":old_production_rate"),
      (party_set_slot, ":center_no", ":item_no", ":production_rate"),
  ]),
]
