MENUS = [
("camp_action", mnf_scale_picture|mnf_enable_hot_keys,
   "Choose an action:",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("camp_quick_start", [], "Quick start.",
        [
          (jump_to_menu, "mnu_quick_start"),
        ]
      ),
	  
      ("camp_retire", [], "Retire from adventuring.",
        [
          (jump_to_menu, "mnu_retirement_verify"),
        ]
      ),

### NEW: attempt to replace every regular in the game with new instances to update their stats ###
### FAILS: you must start a new game to get new troop stats ###
      ("fix_regulars", [(eq, "$g_sod_debug", 1), (eq, 1, 0)], "DEBUG: Replace all troops from prototypes [DANGEROUS].",
        [
          # generate the count of instances
          (try_for_parties, ":party"),

            (str_store_party_name_link, s1, ":party"),
            (display_message, "@Refreshing {s1}", powder_blue),

            # iterate over all the members in each party
            (assign, ":index", 0),
            (party_get_num_companion_stacks, ":num_stacks", ":party"),
            (try_for_range, ":unused", 1, ":num_stacks"),
              # get the troop ID
              (party_stack_get_troop_id, ":troop", ":party", ":index"),
              # only regular troops (not characters)
              (try_begin),
                # skip over any heros in the party (this does cause their order to change... but that's tough to avoid (unless we use a temp party & swap)
                (troop_is_hero, ":troop"),
                (val_add, ":index", 1),
              (else_try),
                # replace the entire stack with a newly minted one (at the end of the party)
                (party_stack_get_size, ":count", ":party", ":index"),
                (party_remove_members, ":party", ":troop", ":count"),
                (party_add_members, ":party", ":troop", ":count"),
              (try_end),
            (try_end),

            # iterate over all the prisoner stacks in each party
            (assign, ":index", 0),
            (party_get_num_prisoner_stacks, ":num_stacks", ":party"),
            (try_for_range, ":unused", 1, ":num_stacks"),
              # get the troop ID
              (party_prisoner_stack_get_troop_id, ":troop", ":party", ":index"),
              # only regular troops (not characters)
              (try_begin),
                # skip over any heros in the party (this does cause their order to change... but that's tough to avoid (unless we use a temp party & swap)
                (troop_is_hero, ":troop"),
                (val_add, ":index", 1),
              (else_try),
                # replace the entire stack with a newly minted one (at the end of the party)
                (party_prisoner_stack_get_size, ":count", ":party", ":index"),
                (party_remove_prisoners, ":party", ":troop", ":count"),
                (party_add_prisoners, ":party", ":troop", ":count"),
              (try_end),
            (try_end),

          (try_end),
        ]
      ),

      ("fix_dups", [(eq, "$g_fix_dup_troops", 0)], "FIX: Remove duplicate lords!",
        [
          (display_message, "@FINDING & FIXING DUPLICATE LORDS...", debug_color),

          # generate the count of instances
          (try_for_parties, ":party"),
            (neg|is_between, ":party", "p_temp_party", "p_town_merc_1"), # don't consider temp parties (they have duplicates by definition)
            (party_get_num_companion_stacks, ":num_stacks", ":party"),
            (try_for_range, ":i_stack", 0, ":num_stacks"),
              (party_stack_get_troop_id, ":troop", ":party", ":i_stack"),
              (troop_is_hero, ":troop"), # only heros - regulars aren't unique
              (troop_get_slot, ":count", ":troop", troop_slot_instances),
              (val_add, ":count", 1),
              (troop_set_slot, ":troop", troop_slot_instances, ":count"),
            (try_end),
          (try_end),

          # keep track of count of fixed troops
          (assign, ":fixed", 0),

          # for each duplicated hero, delete occurrences where they're not the leader of that party
          (try_for_parties, ":party"),
            (neg|is_between, ":party", "p_temp_party", "p_town_merc_1"), # don't consider temp parties (they have duplicates by definition)
            (party_get_num_companion_stacks, ":num_stacks", ":party"),
            (try_for_range, ":i_stack", 1, ":num_stacks"),
              (party_stack_get_troop_id, ":troop", ":party", ":i_stack"),
              (troop_is_hero, ":troop"),
              (try_begin),
                (troop_slot_ge, ":troop", troop_slot_instances, 2),

                # kill this duplicate copy!
                (party_stack_get_size, ":count", ":party", ":i_stack"),
                (party_remove_members, ":party", ":troop", ":count"),

                # document the change
                (assign, reg1, ":count"),
                (store_sub, reg0, ":count", 1),
                (str_store_troop_name_by_count, s1, ":troop", ":count"),
                (str_store_party_name, s2, ":party"),
                (display_message, "@{reg0?{reg1} {s1}:{s1}} in {s2} ...deleted", red),
                (val_add, ":fixed", 1),

                # adjust indexes for removing this stack
                (val_sub, ":i_stack", 1), #NOTE: this doesn't really work... only the end can be modified, not the index variable
                (val_sub, ":num_stacks", 1),

                # adjust the count of instances of this hero
                (troop_get_slot, ":instances", ":troop", troop_slot_instances),
                (val_sub, ":instances", 1),
                (troop_set_slot, ":troop", troop_slot_instances, ":instances"),

              (try_end),
            (try_end),
          (try_end),

          # reset the counts
          (try_for_parties, ":party"),
            (party_get_num_companion_stacks, ":num_stacks", ":party"),
            (neg|is_between, ":party", "p_temp_party", "p_town_merc_1"), # don't consider temp parties (they have duplicates by definition)
            (try_for_range, ":i_stack", 0, ":num_stacks"),
              (party_stack_get_troop_id, ":troop", ":party", ":i_stack"),
              (troop_is_hero, ":troop"),
              (troop_set_slot, ":troop", troop_slot_instances, 0),
            (try_end),
          (try_end),

          # report analysis
          (assign, reg0, ":fixed"),
          (try_begin),
            (eq, reg0, 0),
            (display_message, "@No duplicates found! :)", green),
            (assign, "$g_fix_dup_troops", 1),
          (else_try),
            (display_message, "@Fixed {reg0} duplicates", debug_color),
          (try_end),
        ]
      ),

      ("camp_action_4", [], "Back to camp menu.",
        [
          (jump_to_menu, "mnu_camp"),
        ]
      ),
    ]
  ),
]
