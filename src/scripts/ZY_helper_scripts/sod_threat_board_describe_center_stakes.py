# COST: trivial
SCRIPTS = [
("sod_threat_board_describe_center_stakes",
 [
   (store_script_param_1, ":center_no"),

   (party_get_slot, ":population", ":center_no", slot_center_sod_local_population),
   (party_get_slot, ":health", ":center_no", slot_center_sod_local_health),
   (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
   (party_get_slot, ":local_prosperity", ":center_no", slot_center_sod_local_prosperity),
   (party_get_slot, ":wealth", ":center_no", slot_town_wealth),
   (assign, ":cattle", 0),
   (try_begin),
     (party_slot_eq, ":center_no", slot_party_type, spt_village),
     (party_get_slot, ":cattle", ":center_no", slot_village_number_of_cattle),
   (try_end),

    (assign, reg(11), ":population"),
    (assign, reg(12), ":health"),
    (assign, reg(13), ":prosperity"),
    (assign, reg(14), ":local_prosperity"),
    (assign, reg(15), ":wealth"),
    (assign, reg(16), ":cattle"),

   (try_begin),
     (party_slot_eq, ":center_no", slot_party_type, spt_village),
     (str_store_string, s8, "@Local ledger: {reg11} people, health {reg12}, prosperity {reg13}, local reserves {reg14}, wealth {reg15}, {reg16} cattle."),
   (else_try),
     (str_store_string, s8, "@Local ledger: {reg11} people, health {reg12}, prosperity {reg13}, local reserves {reg14}, wealth {reg15}."),
   (try_end),
 ]),
]
