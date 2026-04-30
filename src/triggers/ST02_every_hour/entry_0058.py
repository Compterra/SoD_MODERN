SIMPLE_TRIGGERS = [
(2,
   [
       (store_troop_gold, ":total_value", "trp_player"),
       (store_div, ":bandit_attraction", ":total_value", (10000/100)), #10000 gold = excellent_target

       (troop_get_inventory_capacity, ":inv_size", "trp_player"),
       (try_for_range, ":i_slot", 0, ":inv_size"),
         (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
         (ge, ":item_id", 0),
         (try_begin),
           (is_between, ":item_id", trade_goods_begin, trade_goods_end),
           (store_item_value, ":item_value", ":item_id"),
           (val_add, ":total_value", ":item_value"),
         (try_end),
       (try_end),
       (val_clamp, ":bandit_attraction", 0, 101),
       (party_set_bandit_attraction, "p_main_party", ":bandit_attraction"),
    ]),
]
