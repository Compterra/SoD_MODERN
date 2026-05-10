MENUS = [
(
    "seven_ash_mirelle_low_lantern", mnf_disable_all_keys,
    "The Low Lantern tavern keeps its best room shuttered and its worst table near the kitchen door. Mirelle Voss sits where she can see every exit. Tib, a thin boy with river mud on his cuffs, carries a folded scrap too carefully for an errand he understands.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (str_store_party_name, s11, "p_town_5"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_mirelle_evidence, sod_seven_ash_evidence_witness),
    ],
    [
      ("seven_ash_mirelle_talk", [
        (eq, "$current_town", "p_town_5"),
      ], "Let Mirelle handle Tib, then speak with her.", [
        (start_map_conversation, "trp_seven_ash_mirelle_voss"),
      ]),
      ("seven_ash_mirelle_travel_needed", [
        (neq, "$current_town", "p_town_5"),
      ], "Travel to {s11}; Mirelle is not here.", [
        (jump_to_menu, "mnu_start_phase_2"),
      ]),
      ("seven_ash_mirelle_back", [], "Return to the recruitment board.", [
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

