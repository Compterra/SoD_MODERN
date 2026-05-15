MENUS = [
(
    "event_02", mnf_disable_all_keys,
    "Tales of your honor spread around the country. Everywhere you go, your procession is surrounded by beggars.",
    "none",
    [

    ],
    [
      ("choice_02_1", [], "Set aside 200 denars for alms.",
       [
          (store_troop_gold, ":gold", "trp_player"),
       (try_begin),
        (ge, ":gold", 200),
        (call_script, "script_change_player_honor", 3),
        (call_script, "script_change_troop_renown", "trp_player", 10),
        (call_script, "script_sod_player_charge_gold", 200),
        (else_try),
        (display_message, "@You don't have enough gold for alms. The crowd leaves disappointed.", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
        (try_end),
        (change_screen_return),
        ]
       ),
      ("choice_02_2", [], "Ignore them.",
       [
       (call_script, "script_change_troop_renown", "trp_player", -5),
       (call_script, "script_change_player_honor", -5),
        (change_screen_return),
        ]
       ),
      ("choice_02_3", [], "Drive them away.",
       [
       (call_script, "script_change_player_honor", -4),
       (change_screen_return),
        ]
       ),
      ]
  ),
]
