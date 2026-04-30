SCRIPTS = [
("sod_quest_battle_scan_agents",
    [
      (try_for_agents, ":agent_no"),
        (agent_get_slot, ":was_alive", ":agent_no", slot_agent_is_alive_before_retreat),
        (try_begin),
          (agent_is_alive, ":agent_no"),
          (eq, ":was_alive", 0),
          (agent_set_slot, ":agent_no", slot_agent_is_alive_before_retreat, 1),
        (else_try),
          (eq, ":was_alive", 1),
          (neg|agent_is_alive, ":agent_no"),
          (agent_set_slot, ":agent_no", slot_agent_is_alive_before_retreat, 2),
          (call_script, "script_sod_quest_battle_agent_defeated", ":agent_no", -1, 0),
        (try_end),
      (try_end),
  ]),
]
