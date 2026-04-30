SCRIPTS = [
("troop_add_gold",
        [(store_script_param, ":troop_no", 1),
          (store_script_param, ":amount", 2),
          (troop_add_gold, ":troop_no", ":amount"),
          (try_begin),
            (eq, ":troop_no", "trp_player"),
            (play_sound, "snd_money_received"),
          (try_end),
      ]),
]
