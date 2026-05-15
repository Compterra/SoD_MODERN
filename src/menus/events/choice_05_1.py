MENUS = [
(
    "event_05", mnf_disable_all_keys,
    "A local agitator is spreading false rumors about you. Most are nonsense, but enough people believe them that rival courts may use the stories against you.",
    "none",
    [

    ],
    [
      ("choice_05_1", [], "Let him speak. A ruler should not fear every loose tongue.",
       [
          (call_script, "script_change_badboy_rating", 3), 
    	  (call_script, "script_change_player_honor", 2),
          (call_script, "script_change_troop_renown", "trp_player", -25),
          (change_screen_return),
        ]
       ),
      ("choice_05_2", [], 
	  "Pay a royal scribe 300 denars to counter the rumors.",
       [
        (store_troop_gold, ":gold", "trp_player"),
        (try_begin),
          (ge, ":gold", 300),
          (call_script, "script_change_player_honor", 2), 
          (call_script, "script_change_troop_renown", "trp_player", 25),
          (call_script, "script_sod_player_charge_gold", 300),
        (else_try),
          (display_message, "@You don't have enough gold. The rumors continue to spread.", quest_fail_color),
          (call_script, "script_change_badboy_rating", 2),
          (call_script, "script_change_troop_renown", "trp_player", -5),
        (try_end),
        (change_screen_return),
        ]
       ),
      ("choice_05_3", [], "Offer him 100 denars to stop talking.",
       [
        (store_troop_gold, ":gold", "trp_player"),
        (try_begin),
        (ge, ":gold", 100),
        (call_script, "script_sod_player_charge_gold", 100),
        (else_try),
        (display_message, "@You don't have enough gold. He keeps talking.", quest_fail_color),
        (call_script, "script_change_badboy_rating", 3), 
        (call_script, "script_change_troop_renown", "trp_player", -7),
        (try_end),
       (change_screen_return),
        ]
       ),
       ("choice_05_4", [], "Throw him into the dungeon. Insulting the crown is a crime.",
       [
       (call_script, "script_change_player_honor", -5),
       (change_screen_return),
        ]
       ),
       ("choice_05_5", [], "Silence him permanently and seize his property.",
       [
       (call_script, "script_change_player_honor", -10),
       (troop_add_gold, "trp_player", 1000),
       (change_screen_return),
        ]
       ),
      ]
  ),
]
