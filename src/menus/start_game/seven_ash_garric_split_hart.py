MENUS = [
(
    "seven_ash_garric_split_hart", mnf_disable_all_keys,
    "The Split Hart tavern goes quiet around Garric Ashbow before you see him: a scarred archer with his back to the wall, counting exits by habit. Eda Flint wipes the same cup three times and watches whether you speak like a buyer, a judge, or a captain.^^This menu frames the scene; the recruitment choice belongs to dialogue with Garric.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (str_store_party_name, s11, "p_town_6"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_garric_evidence, sod_seven_ash_evidence_witness),
    ],
    [
      ("seven_ash_garric_talk", [
        (eq, "$current_town", "p_town_6"),
      ], "Enter the tavern and speak with Garric.", [
        (start_map_conversation, "trp_seven_ash_garric_ashbow"),
      ]),
      ("seven_ash_garric_travel_needed", [
        (neq, "$current_town", "p_town_6"),
      ], "Travel to {s11}; Garric is not here.", [
        (jump_to_menu, "mnu_start_phase_2"),
      ]),
      ("seven_ash_garric_back", [], "Return to the recruitment board.", [
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

