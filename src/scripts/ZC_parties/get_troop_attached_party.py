SCRIPTS = [
("get_troop_attached_party",
    [
      (store_script_param_1, ":troop_no"),

      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (assign, ":attached_party_no", -1),
      (try_begin),
        (ge, ":party_no", 0),
        (party_get_attached_to, ":attached_party_no", ":party_no"),
      (try_end),
      (assign, reg0, ":attached_party_no"),
  ]),
]
