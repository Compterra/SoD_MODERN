DIALOGS = [
[anyone, "boar_clan_recruit_2",
   [
      (store_encountered_party, ":party"),
	  
	  (assign, ":total_cost", 0),
	  (party_get_num_companion_stacks, ":num_stacks", ":party"),
        (try_for_range, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop", ":party", ":i_stack"),
          (party_stack_get_size, ":stack_size", ":party", ":i_stack"),
          (call_script, "script_game_get_join_cost", ":stack_troop"),
          (assign, ":cur_cost", reg0),
          (val_mul, ":cur_cost", ":stack_size"),
		  (val_add, ":total_cost", ":cur_cost"),
        (try_end),
      (assign, reg5, ":total_cost"),
   ], "Now that's the spirit I like! Come 'ere lads, this is an offer to consider...! We are ready to follow you for, let's say {reg5} denars.", "boar_clan_recruit_3", [],],
]
