MENUS = [
(
    "seven_ash_mirelle_evacuation_routes", mnf_disable_all_keys,
    "Mirelle stands behind Ashwick's kitchens with chalk, thread, and three women who do not ask questions twice. She marks pig pens, fence boards, cellar mouths, and the paths frightened people will remember when shouting begins.",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_w"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_mirelle),
    ],
    [
      ("seven_ash_mirelle_return_talk", [], "Walk the hidden routes with Mirelle.", [
        (start_map_conversation, "trp_seven_ash_mirelle_voss"),
      ]),
      ("seven_ash_mirelle_return_back", [], "Return to the recruitment board.", [
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_none),
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

