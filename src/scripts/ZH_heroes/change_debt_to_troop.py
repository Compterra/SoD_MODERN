SCRIPTS = [
("change_debt_to_troop",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":new_debt"),

      (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt),
      (assign, reg1, ":cur_debt"),
      (val_add, ":cur_debt", ":new_debt"),
      (assign, reg2, ":cur_debt"),
      (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),
      (call_script, "script_store_troop_name_link_fief", s1, ":troop_no"),
      (display_message, "@You now owe {reg2} denars to {s1}.", dark_red),
  ]),
]
