MENUS = [
(
    "event_01", mnf_disable_all_keys,
    "A minstrel composed a song about your noble deeds.",
    "none",
    [

    ],
    [
      ("choice_01_1", [], "Excellent!",
       [
          (call_script, "script_change_troop_renown", "trp_player", 10),
          (change_screen_return),
        ]
       ),
      ("choice_01_2", [], "Reward him with 200 denars. Let his song be played across the land.",
       [
       (store_troop_gold, ":gold", "trp_player"),
       (try_begin),
        (ge, ":gold", 200),
        (call_script, "script_change_troop_renown", "trp_player", 20),
        (call_script, "script_sod_player_charge_gold", 200),
       (else_try),
        (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
       (try_end),
       (change_screen_return),
       ]
       ),
      ("choice_01_3", [], "Noble deeds? A song? Bring me this fool's head!",
       [
       (call_script, "script_change_player_honor", -5),
       (change_screen_return),
        ]
       ),
      ]
  ),
]
