SCRIPTS = [
("lord_comment_to_s43",
        [(store_script_param, ":lord", 1),
          (store_script_param, ":default_string", 2),

          (troop_get_slot, ":reputation", ":lord", slot_lord_reputation_type),
          (val_add, ":reputation", ":default_string"),
          (str_store_string, 43, ":reputation"),
      ]),
]
