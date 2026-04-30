SCRIPTS = [
("update_ransom_brokers",
      [(try_for_range, ":town_no", towns_begin, towns_end),
          (party_set_slot, ":town_no", slot_center_ransom_broker, 0),
        (try_end),

        (try_for_range, ":troop_no", ransom_brokers_begin, ransom_brokers_end),
          (store_random_in_range, ":town_no", towns_begin, towns_end),
          (party_set_slot, ":town_no", slot_center_ransom_broker, ":troop_no"),
        (try_end),

        (party_set_slot, "p_town_2", slot_center_ransom_broker, "trp_ramun_the_slave_trader"),
    ]),
]
