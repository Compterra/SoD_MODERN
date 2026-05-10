MENUS = [
(
    "seven_ash_garric_watch_platform", mnf_disable_all_keys,
    "Ashwick's old watch platform creaks above the south road. Garric climbs it without admiring the view, tapping each board with his heel and naming every place an archer would die if pride chose the repairs.",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_w"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_garric),
    ],
    [
      ("seven_ash_garric_return_talk", [], "Let Garric set the firing lanes.", [
        (start_map_conversation, "trp_seven_ash_garric_ashbow"),
      ]),
      ("seven_ash_garric_return_back", [], "Return to the recruitment board.", [
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_none),
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

