MENUS = [
(
    "seven_ash_tomas_militia_yard", mnf_disable_all_keys,
    "Tomas watches Ashwick's militia hold spears like broom handles. He studies elbows, feet, breath, and the way fear travels from one row to another before the first command is given.",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_w"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_tomas),
    ],
    [
      ("seven_ash_tomas_return_talk", [], "Let Tomas begin the first drill.", [
        (start_map_conversation, "trp_seven_ash_tomas_reed"),
      ]),
      ("seven_ash_tomas_return_back", [], "Return to the recruitment board.", [
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_none),
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

