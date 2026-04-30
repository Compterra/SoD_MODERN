SCRIPTS = [
("change_troop_renown",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":renown_change"),

      (troop_get_slot, ":old_renown", ":troop_no", slot_troop_renown),
      (store_add, ":new_renown", ":old_renown", ":renown_change"),
      (val_max, ":new_renown", 0),
      (troop_set_slot, ":troop_no", slot_troop_renown, ":new_renown"),

      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (call_script, "script_store_troop_name_link", s1, ":troop_no"),
        (assign, reg12, ":renown_change"),
        (val_abs, reg12),
        (try_begin),
          (gt, ":renown_change", 0),
          (display_message, "@You gained {reg12} renown.", renown_color),
        (else_try),
          (lt, ":renown_change", 0),
          (display_message, "@You lose {reg12} renown.", lose_renown_color),
        (try_end),
      (try_end),
      (call_script, "script_update_troop_notes", ":troop_no"),
  ]),
]
