MENUS = [
(
    "event_05", mnf_disable_all_keys,
    "A local naysayer is spreading false rumors about you. While most of the stories are just pure nonsense, they may offer other nations reasons to attack you.",
    "none",
    [

    ],
    [
      ("choice_05_1", [], "Let him speak what he wants. Every man has his rights.",
       [
          (call_script, "script_change_badboy_rating", 3), 
    	  (call_script, "script_change_player_honor", 2),
          (call_script, "script_change_troop_renown", "trp_player", -25),
          (change_screen_return),
        ]
       ),
      ("choice_05_2", [ (store_troop_gold, ":gold", "trp_player"),(ge, ":gold", 300)], 
	  "Tell royal scribe to spread opposite rumors to counter his lies. It will cost 300 denars.",
       [
        (call_script, "script_change_player_honor", 2), 
        (call_script, "script_change_troop_renown", "trp_player", 25),
        (call_script, "script_sod_player_charge_gold", 300),
        (change_screen_return),
        ]
       ),
      ("choice_05_3", [], "Ask him to stop. 100 denars might help him to forget what he said.",
       [
        (store_troop_gold, ":gold", "trp_player"),
        (try_begin),
        (ge, ":gold", 100),
        (call_script, "script_sod_player_charge_gold", 100),
        (else_try),
        (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
        (call_script, "script_change_badboy_rating", 3), 
        (call_script, "script_change_troop_renown", "trp_player", -7),
        (try_end),
       (change_screen_return),
        ]
       ),
       ("choice_05_4", [], "Throw him into the dungeon. Insulting the King is a crime.",
       [
       (call_script, "script_change_player_honor", -5),
       (change_screen_return),
        ]
       ),
       ("choice_05_5", [], "Silence him permanently and seize his house and properties.",
       [
       (call_script, "script_change_player_honor", -10),
       (troop_add_gold, "trp_player", 1000),
       (change_screen_return),
        ]
       ),
      ]
  ),
]
