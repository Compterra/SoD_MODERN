SCRIPTS = [
("sod_party_is_safe_active_to_reg",
 [
   (store_script_param_1, ":party_no"),
   (assign, reg0, 0),
   (try_begin),
     (ge, ":party_no", 0),
     (party_is_active, ":party_no"),
     (neg|party_slot_eq, ":party_no", slot_party_type, spt_companion_retinue),
     (assign, reg0, 1),
   (try_end),
 ]),
]
