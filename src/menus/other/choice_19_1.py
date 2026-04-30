MENUS = [
(
    "event_18", mnf_disable_all_keys,
    "While you ride firmly ahead, you overhear some of your men starting an argument about the loot. Before you can do anything, the argument scalates into a fight and soon afterwards into a massive brawl. You...",
    "none",
    [
    ],
    [
      ("choice_19_1", [], "Let them fight.", [
    (call_script, "script_change_player_party_morale", -5),

          (change_screen_return),
        ]
       ),
           ("choice_19_2", [], "Order your troops to stop the fight immediatly.", [
       (call_script, "script_change_player_party_morale", -5),
          (change_screen_return),
        ]
       ),
           ("choice_19_3", [], "Punish the responsible ones by taking loot to yourself.", [
       (call_script, "script_change_player_party_morale", -20),
          (change_screen_return),
        ]
       ),
      ]
  ),
]
