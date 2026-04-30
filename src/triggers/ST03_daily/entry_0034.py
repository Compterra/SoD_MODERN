SIMPLE_TRIGGERS = [
(24,
   [
      (try_for_range, ":village_no", villages_begin, villages_end),
        (call_script, "script_refresh_village_merchant_inventory", ":village_no"),
      (try_end),
    ]),
]
