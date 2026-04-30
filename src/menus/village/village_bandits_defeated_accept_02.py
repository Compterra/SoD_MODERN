MENUS = [
(
    "village_revenge_succeded", mnf_disable_all_keys,
    "In a battle worthy of song, you and your men drive the enemy out of the village.",
    "none",
    [(party_get_slot, ":bandit_troop", "$g_encountered_party", slot_village_infested_by_bandits),
     (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
     (party_clear, "p_temp_party"),
     (party_add_members, "p_temp_party", ":bandit_troop", "$qst_eliminate_bandits_infesting_village_num_bandits"),
     (assign, "$g_strength_contribution_of_player", 50),
     (call_script, "script_party_give_xp_and_gold", "p_temp_party"),
       (call_script, "script_succeed_quest", "qst_jotnar_clan_revenge"),
       (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 3),
    ],
    [
      ("village_bandits_defeated_accept", [], "Continue...", [(jump_to_menu, "mnu_village")]),
    ],
  ),
]
