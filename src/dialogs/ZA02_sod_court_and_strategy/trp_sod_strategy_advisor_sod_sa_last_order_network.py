DIALOGS = [
[trp_sod_strategy_advisor, "sod_sa_last_order_network", [
    (quest_get_slot, ":focus_center", "qst_companion_cassian_last_order", slot_quest_sod_runtime_last_center),
    (try_begin),
      (is_between, ":focus_center", centers_begin, centers_end),
      (str_store_party_name, s3, ":focus_center"),
    (else_try),
      (str_store_string, s3, "@an old frontier cache"),
    (try_end),
], "The order names a dead drop near {s3}. Not coin, not weapons. Names. Families. Informants. Couriers who wore Imperial colors because your father asked them to survive long enough to matter. Some may still be alive.", "sod_sa_last_order_choice", []],
]
