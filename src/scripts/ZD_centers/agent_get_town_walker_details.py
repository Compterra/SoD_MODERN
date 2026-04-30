SCRIPTS = [
("agent_get_town_walker_details",
      [(store_script_param, ":agent_no", 1),
        (agent_get_entry_no, ":entry_no", ":agent_no"),
        (store_sub, ":walker_no", ":entry_no", town_walker_entries_start),

        (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
        (party_get_slot, ":walker_type", "$current_town", ":type_slot"),
        (store_add, ":dna_slot", slot_center_walker_0_dna,  ":walker_no"),
        (party_get_slot, ":walker_dna", "$current_town", ":dna_slot"),
        (assign, reg0, ":walker_type"),
        (assign, reg1, ":walker_dna"),
        (assign, reg2, ":walker_no"),
    ]),
]
