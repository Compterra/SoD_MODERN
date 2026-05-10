MENUS = [
(
    "seven_ash_aldrik_gate", mnf_disable_all_keys,
    "Aldrik stands before Ashwick's gate with his shield under one arm. The village watches too eagerly, hungry for the old promise that a painted board and one sworn man can make fear behave.",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_w"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_aldrik),
    ],
    [
      ("seven_ash_aldrik_return_talk", [], "Let Aldrik place his shield.", [
        (start_map_conversation, "trp_seven_ash_sir_aldrik_vane"),
      ]),
      ("seven_ash_aldrik_return_back", [], "Return to the recruitment board.", [
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_none),
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

