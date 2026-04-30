SCRIPTS = [
("sod_quest_battle_mission_start",
    [
      (store_mission_timer_a, ":mission_time"),
      (try_for_agents, ":agent_no"),
        (try_begin),
          (agent_is_alive, ":agent_no"),
          (agent_set_slot, ":agent_no", slot_agent_is_alive_before_retreat, 1),
        (else_try),
          (agent_set_slot, ":agent_no", slot_agent_is_alive_before_retreat, 0),
        (try_end),
      (try_end),
      (try_for_range, ":quest_no", all_quests_begin, all_quests_end),
        (check_quest_active, ":quest_no"),
        (quest_set_slot, ":quest_no", slot_quest_sod_runtime_state, sod_quest_state_active),
        (quest_set_slot, ":quest_no", slot_quest_sod_runtime_last_event, sod_quest_event_mission),
        (quest_set_slot, ":quest_no", slot_quest_sod_battle_timer_start, ":mission_time"),
        (try_begin),
          (quest_slot_ge, ":quest_no", slot_quest_sod_battle_action, 1),
          (quest_slot_eq, ":quest_no", slot_quest_sod_battle_required, 0),
          (quest_set_slot, ":quest_no", slot_quest_sod_battle_required, 1),
        (try_end),
      (try_end),
      (call_script, "script_sod_quest_dispatch_active_event", sod_quest_event_mission, -1, "$g_enemy_party", -1),
  ]),
]

script_sod_quest_battle_mission_start = SCRIPTS[0][1]
SCRIPT = script_sod_quest_battle_mission_start