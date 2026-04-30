MENUS = [
(
    "town_bandits_succeeded", mnf_disable_all_keys,
    "The bandits fall before you as wheat to a scythe! Soon you stand alone in the streets while most of your attackers lie unconscious, dead or dying."\
    " Searching the bodies, you find a purse which must have belonged to a previous victim of these brutes. Or perhaps, it was given to them by someone who wanted to arrange a suitable ending to your life.",
    "none",
    [
      (party_set_slot, "$current_town", slot_center_has_bandits, 0),
      (assign, "$g_last_defeated_bandits_town", "$g_encountered_party"),
      (try_begin),
        (check_quest_active, "qst_deal_with_night_bandits"),
        (neg|check_quest_succeeded, "qst_deal_with_night_bandits"),
        (quest_slot_eq, "qst_deal_with_night_bandits", slot_quest_target_center, "$g_encountered_party"),
        (call_script, "script_succeed_quest", "qst_deal_with_night_bandits"),
      (try_end),
      (store_mul, ":xp_reward", "$num_center_bandits", 117),
      (add_xp_to_troop, ":xp_reward", "trp_player"),
      (store_mul, ":gold_reward", "$num_center_bandits", 50),
      (call_script, "script_troop_add_gold", "trp_player", ":gold_reward"),
    ],
    [
      ("continue", [], "Continue...", [(change_screen_return)]),
    ],
  ),
]
