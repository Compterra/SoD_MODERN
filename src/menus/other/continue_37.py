MENUS = [
(
    "collect_taxes_complete", mnf_disable_all_keys,
    "You've collected {reg13} denars in taxes from {s3}. {s19} will be expecting you to take the money to him.",
    "none",
    [(str_store_party_name, s3, "$current_town"),
     (quest_get_slot, ":quest_giver", "qst_collect_taxes", slot_quest_giver_troop),
     (call_script, "script_store_troop_name", s19, ":quest_giver"),
     (quest_get_slot, reg13, "qst_collect_taxes", slot_quest_gold_reward),
     (try_begin),
       (eq, "$qst_collect_taxes_halve_taxes", 0),
       (call_script, "script_change_player_relation_with_center", "$current_town", -2),
     (try_end),
     (call_script, "script_succeed_quest", "qst_collect_taxes"),
     ],
    [
      ("continue", [], "Continue...",
       [(change_screen_return),
        ]),
    ]
  ),
]
