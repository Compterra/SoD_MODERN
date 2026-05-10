MENUS = [
(
    "seven_ash_beren_gate", mnf_disable_all_keys,
    "Beren stands in Ashwick's gate and tests the beam with his shoulder. A child hides behind Mother Hilda. Beren notices, steps away from the gate, and looks angry that distance is the only apology he knows.",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_w"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_beren),
    ],
    [
      ("seven_ash_beren_return_talk", [], "Let Beren mark the breach point.", [
        (start_map_conversation, "trp_seven_ash_beren_hardhand"),
      ]),
      ("seven_ash_beren_return_back", [], "Return to the recruitment board.", [
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_none),
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

