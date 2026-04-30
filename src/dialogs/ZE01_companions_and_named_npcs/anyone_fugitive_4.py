DIALOGS = [
[anyone, "fugitive_4", [], "Damn you! You will not be going anywhere!", "close_window",
   [(set_party_battle_mode),
    (try_for_agents, ":cur_agent"),
      (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
      (eq, ":cur_agent_troop", "trp_fugitive"),
      (agent_set_team, ":cur_agent", 1),
    (try_end),
    (quest_set_slot, "qst_hunt_down_fugitive", slot_quest_current_state, 1),
    ]],
]
