MENUS = [
(
    "seven_ash_elianor_infirmary", mnf_disable_all_keys,
    "Elianor stands in Ashwick's church with Mother Hilda, the granary tally, and a list of every cellar that stays dry. No one calls it an infirmary yet, but the benches have already been moved.",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_w"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_elianor),
    ],
    [
      ("seven_ash_elianor_return_talk", [], "Give Elianor the church key.", [
        (start_map_conversation, "trp_seven_ash_sister_elianor"),
      ]),
      ("seven_ash_elianor_return_back", [], "Return to the recruitment board.", [
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_none),
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

