SCRIPTS = [
("change_player_party_morale",
    [
      (store_script_param_1, ":morale_dif"),
      (party_get_morale, ":cur_morale", "p_main_party"),
      (store_add, ":new_morale", ":cur_morale", ":morale_dif"),
      (val_clamp, ":new_morale", 0, 101),
      (party_set_morale, "p_main_party", ":new_morale"),
      (try_begin),
        (lt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":cur_morale", ":new_morale"),
        (display_message, "str_party_lost_morale", lose_morale_color),
      (else_try),
        (gt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":new_morale", ":cur_morale"),
        (display_message, "str_party_gained_morale", gain_morale_color),
      (try_end),
  ]),
]
