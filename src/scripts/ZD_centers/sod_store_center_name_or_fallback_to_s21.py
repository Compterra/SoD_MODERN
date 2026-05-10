SCRIPTS = [
("sod_store_center_name_or_fallback_to_s21",
 [
   (store_script_param_1, ":center_no"),
   (store_script_param_2, ":fallback_string"),
   (try_begin),
     (is_between, ":center_no", centers_begin, centers_end),
     (str_store_party_name_link, s21, ":center_no"),
   (else_try),
     (str_store_string, s21, ":fallback_string"),
   (try_end),
 ]),
]
