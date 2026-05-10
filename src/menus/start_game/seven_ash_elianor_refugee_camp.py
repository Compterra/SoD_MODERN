MENUS = [
(
    "seven_ash_elianor_refugee_camp", mnf_disable_all_keys,
    "Saint Ormond's refugee camp lies in old sheep barns and rain-cut lanes. Sister Elianor washes blood from a boy's hair with water already used twice. The wounded cannot march, widows ask for knives, children ask for bread, and two men who want to fight cannot stand in formation.",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_w"),
      (str_store_party_name, s11, "p_village_7"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_elianor_evidence, sod_seven_ash_evidence_witness),
    ],
    [
      ("seven_ash_elianor_talk", [
        (eq, "$current_town", "p_village_7"),
      ], "Inspect the camp, then speak with Sister Elianor.", [
        (start_map_conversation, "trp_seven_ash_sister_elianor"),
      ]),
      ("seven_ash_elianor_travel_needed", [
        (neq, "$current_town", "p_village_7"),
      ], "Travel to {s11}; Sister Elianor is not here.", [
        (jump_to_menu, "mnu_start_phase_2"),
      ]),
      ("seven_ash_elianor_back", [], "Return to the recruitment board.", [
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

