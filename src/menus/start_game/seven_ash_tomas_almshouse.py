MENUS = [
(
    "seven_ash_tomas_almshouse", mnf_disable_all_keys,
    "The Red Crutch almshouse smells of boiled linen, boot grease, and old rain. Tomas Reed mends a split boot beside men who either owe him their lives or hate him for the price. Old Jory nods toward him. Matteo will not look up.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (str_store_party_name, s11, "p_town_3"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_tomas_evidence, sod_seven_ash_evidence_witness),
    ],
    [
      ("seven_ash_tomas_talk", [
        (eq, "$current_town", "p_town_3"),
      ], "Hear Old Jory and Matteo, then speak with Tomas.", [
        (start_map_conversation, "trp_seven_ash_tomas_reed"),
      ]),
      ("seven_ash_tomas_travel_needed", [
        (neq, "$current_town", "p_town_3"),
      ], "Travel to {s11}; Tomas is not here.", [
        (jump_to_menu, "mnu_start_phase_2"),
      ]),
      ("seven_ash_tomas_back", [], "Return to the recruitment board.", [
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

