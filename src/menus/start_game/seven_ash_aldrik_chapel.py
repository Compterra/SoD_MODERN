MENUS = [
(
    "seven_ash_aldrik_chapel", mnf_disable_all_keys,
    "Saint Cuthbert's Wayside Chapel has a cracked bell, a poor alms box, and a knight polishing a dented helm beside the road. A boy offers Sir Aldrik Vane an apple. Aldrik cuts it in half and returns the larger piece. Mara of the Bridge waits near the chapel wall, ready to say what his old accusers would not.",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_w"),
      (str_store_party_name, s11, "p_village_5"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_aldrik_evidence, sod_seven_ash_evidence_witness),
    ],
    [
      ("seven_ash_aldrik_talk", [
        (eq, "$current_town", "p_village_5"),
      ], "Hear Mara, then speak with Aldrik.", [
        (start_map_conversation, "trp_seven_ash_sir_aldrik_vane"),
      ]),
      ("seven_ash_aldrik_travel_needed", [
        (neq, "$current_town", "p_village_5"),
      ], "Travel to {s11}; Aldrik is not here.", [
        (jump_to_menu, "mnu_start_phase_2"),
      ]),
      ("seven_ash_aldrik_back", [], "Return to the recruitment board.", [
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

