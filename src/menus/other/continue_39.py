MENUS = [
(
    "collect_taxes_failed", mnf_disable_all_keys,
    "You could collect only {reg3} denars as tax from {s3} before the revolt broke out. {s1} won't be happy, but some silver will placate him better than nothing at all...",
    "none",
    [(str_store_party_name, s3, "$current_town"),
     (quest_get_slot, ":quest_giver", "qst_collect_taxes", slot_quest_giver_troop),
     (call_script, "script_store_troop_name", s1, ":quest_giver"),
     (quest_get_slot, reg3, "qst_collect_taxes", slot_quest_gold_reward),
     (try_begin),
       (check_quest_active, "qst_collect_taxes"),
       (neg|check_quest_failed, "qst_collect_taxes"),
       (call_script, "script_fail_quest", "qst_collect_taxes"),
       (quest_set_slot, "qst_collect_taxes", slot_quest_current_state, 4),
     (try_end),
     (rest_for_hours, 0, 0, 0), #stop resting
     ],
    [
      ("continue", [], "Continue...",
       [(change_screen_map),
        ]),
    ]
  ),
]
