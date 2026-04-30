SCRIPTS = [
("get_prosperity_text",
        [
          (store_script_param, ":sreg", 1),
          (store_script_param, ":prosperity", 2),
          (val_clamp, ":prosperity", 0, 101),
          (val_div, ":prosperity", 10),
          (val_add, ":prosperity", "str_prosperity_0"),
          (str_store_string, ":sreg", ":prosperity"),
        ]
      ),
]
