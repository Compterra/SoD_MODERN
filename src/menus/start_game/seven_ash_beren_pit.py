MENUS = [
(
    "seven_ash_beren_pit", mnf_disable_all_keys,
    "The mill-yard pit is ringed with cart wheels, rain barrels, and men pretending this is sport. Beren Hardhand fights three at once with a blunted axe. Ansel Miller watches from the flour shed, grief worn thin enough to look like caution.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (str_store_party_name, s11, "p_town_2"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_beren_evidence, sod_seven_ash_evidence_witness),
    ],
    [
      ("seven_ash_beren_talk", [
        (eq, "$current_town", "p_town_2"),
      ], "Hear Ansel Miller, then speak with Beren.", [
        (start_map_conversation, "trp_seven_ash_beren_hardhand"),
      ]),
      ("seven_ash_beren_travel_needed", [
        (neq, "$current_town", "p_town_2"),
      ], "Travel to {s11}; Beren is not here.", [
        (jump_to_menu, "mnu_start_phase_2"),
      ]),
      ("seven_ash_beren_back", [], "Return to the recruitment board.", [
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

