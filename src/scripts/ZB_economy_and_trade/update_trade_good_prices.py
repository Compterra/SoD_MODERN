SCRIPTS = [
("update_trade_good_prices",
    [
      (try_for_range, ":center_no", centers_begin, centers_end),
        (this_or_next|is_between, ":center_no", towns_begin, towns_end),
        (is_between, ":center_no", villages_begin, villages_end),
        (call_script, "script_update_trade_good_price_for_party", ":center_no"),
      (try_end),
      #      (call_script, "script_update_trade_good_price_for_party", "p_zendar"),
      #      (call_script, "script_update_trade_good_price_for_party", "p_salt_mine"),
      #      (call_script, "script_update_trade_good_price_for_party", "p_four_ways_inn"),
  ]),
]
