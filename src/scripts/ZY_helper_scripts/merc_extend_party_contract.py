# COST: trivial
SCRIPTS = [
("merc_extend_party_contract",
 [
   (store_script_param_1, ":party_no"),
   (store_script_param_2, ":term_months"),

   (store_current_day, ":cur_day"),
   (try_begin),
     (ge, ":term_months", 6),
     (store_add, ":new_time", ":cur_day", 187),
   (else_try),
     (ge, ":term_months", 3),
     (store_add, ":new_time", ":cur_day", 97),
   (else_try),
     (store_add, ":new_time", ":cur_day", 37),
   (try_end),
   (party_set_slot, ":party_no", slot_party_merc_contract, ":new_time"),
   (party_set_slot, ":party_no", slot_party_merc_asked, 0),
 ]),
]
