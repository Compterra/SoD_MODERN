SCRIPTS = [
("get_troop_item_amount",
        [(store_script_param, ":troop_no", 1),
          (store_script_param, ":item_no", 2),
          (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
          (assign, ":count", 0),
          (try_for_range, ":i_slot", 0, ":inv_cap"),
            (troop_get_inventory_slot, ":cur_item", ":troop_no", ":i_slot"),
            (eq, ":cur_item", ":item_no"),
            (val_add, ":count", 1),
          (try_end),
          (assign, reg0, ":count"),
      ]),
]
