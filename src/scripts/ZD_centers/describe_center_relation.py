SCRIPTS = [
("describe_center_relation",
    [
      (store_script_param_1, ":sreg"),
      (store_script_param_2, ":relation"),
      (store_add, ":normalized_relation", ":relation", 100),
      (val_add, ":normalized_relation", 5),
      (store_div, ":str_offset", ":normalized_relation", 10),
      (val_clamp, ":str_offset", 0, 20),
      (store_add, ":str_id", "str_center_relation_mnus_100",  ":str_offset"),
      (str_store_string, ":sreg", ":str_id"),
  ]),
]
