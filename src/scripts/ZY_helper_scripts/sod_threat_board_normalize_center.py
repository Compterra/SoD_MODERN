# COST: low
SCRIPTS = [
("sod_threat_board_normalize_center",
 [
   (store_script_param_1, ":center_no"),

   (try_begin),
     (le, ":center_no", 0),
     (call_script, "script_get_closest_center", "p_main_party"),
     (assign, ":center_no", reg0),
   (try_end),

   (try_begin),
     (neg|is_between, ":center_no", centers_begin, centers_end),
     (assign, ":center_no", "p_town_1"),
   (else_try),
     (neg|party_is_active, ":center_no"),
     (call_script, "script_get_closest_center", "p_main_party"),
     (assign, ":center_no", reg0),
     (try_begin),
       (neg|is_between, ":center_no", centers_begin, centers_end),
       (assign, ":center_no", "p_town_1"),
     (try_end),
   (try_end),

   (assign, reg0, ":center_no"),
 ]),
]
