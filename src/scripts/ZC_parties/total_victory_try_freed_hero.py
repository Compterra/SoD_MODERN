SCRIPTS = [
("total_victory_try_freed_hero",
    [
      (assign, reg0, 0),
      (assign, ":stack_troop_dna", 0),
      (party_get_num_prisoner_stacks, ":num_prisoner_stacks", "p_encountered_party_backup"),
      (try_for_range, ":stack_no", "$last_freed_hero", ":num_prisoner_stacks"),
        (eq, reg0, 0),
        (party_prisoner_stack_get_troop_id, ":stack_troop", "p_encountered_party_backup", ":stack_no"),
        (troop_is_hero, ":stack_troop"),
        (party_prisoner_stack_get_troop_dna, ":stack_troop_dna", "p_encountered_party_backup", ":stack_no"),
        (store_add, "$last_freed_hero", ":stack_no", 1),
        (assign, "$talk_context", tc_hero_freed),
        (call_script, "script_setup_troop_meeting", ":stack_troop", ":stack_troop_dna"),
        (assign, reg0, 1),
      (try_end),
  ]),
]
