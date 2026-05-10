MENUS = [
(
    "seven_ash_oswin_palisade", mnf_disable_all_keys,
    "Oswin Ditchwright walks Ashwick's palisade with a string line, a knife, and no mercy for sentimental timber. Villagers follow him at a distance, because every plank he condemns used to belong to someone.",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_w"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_oswin),
    ],
    [
      ("seven_ash_oswin_return_talk", [], "Let Oswin mark the repairs.", [
        (start_map_conversation, "trp_seven_ash_oswin_ditchwright"),
      ]),
      ("seven_ash_oswin_return_back", [], "Return to the recruitment board.", [
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_none),
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

