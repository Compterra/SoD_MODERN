MENUS = [
(
    "seven_ash_sector_commitment", mnf_disable_all_keys,
    "The church map has stopped being an argument and become an order. There are not enough trained bodies to make every sector strong. Choose where Ashwick overcommits, and name which defender's craft leads that sector if they were won.",
    "none",
    [
      (set_background_mesh, "mesh_pic_siege_sighted"),
    ],
    [
      ("seven_ash_sector_outer", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_sector_commitment_locked, 0),
      ], "Strengthen the outer fields, scouts, and road watches. Garric leads if present.", [
        (call_script, "script_sod_seven_ash_commit_sector_focus", sod_seven_ash_sector_outer_fields),
        (jump_to_menu, "mnu_seven_ash_siege_warning"),
      ]),
      ("seven_ash_sector_palisade", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_sector_commitment_locked, 0),
      ], "Strengthen the ditch and palisade. Oswin leads if present.", [
        (call_script, "script_sod_seven_ash_commit_sector_focus", sod_seven_ash_sector_palisade),
        (jump_to_menu, "mnu_seven_ash_siege_warning"),
      ]),
      ("seven_ash_sector_gate", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_sector_commitment_locked, 0),
      ], "Hold the best fighters as gate reserve. Aldrik and Beren lead if present.", [
        (call_script, "script_sod_seven_ash_commit_sector_focus", sod_seven_ash_sector_gate_reserve),
        (jump_to_menu, "mnu_seven_ash_siege_warning"),
      ]),
      ("seven_ash_sector_streets", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_sector_commitment_locked, 0),
      ], "Strengthen the inner streets, fire lanes, and cellars. Mirelle and Elianor lead if present.", [
        (call_script, "script_sod_seven_ash_commit_sector_focus", sod_seven_ash_sector_inner_streets),
        (jump_to_menu, "mnu_seven_ash_siege_warning"),
      ]),
      ("seven_ash_sector_churchyard", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_sector_commitment_locked, 0),
      ], "Strengthen the churchyard fallback. Tomas and Elianor lead if present.", [
        (call_script, "script_sod_seven_ash_commit_sector_focus", sod_seven_ash_sector_churchyard),
        (jump_to_menu, "mnu_seven_ash_siege_warning"),
      ]),
      ("seven_ash_sector_evacuation", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_sector_commitment_locked, 0),
      ], "Strengthen the evacuation escort. Mirelle and Elianor lead if present.", [
        (call_script, "script_sod_seven_ash_commit_sector_focus", sod_seven_ash_sector_evacuation),
        (jump_to_menu, "mnu_seven_ash_siege_warning"),
      ]),
      ("seven_ash_sector_locked", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_sector_commitment_locked, 1),
      ], "Review Nell's final scout report.", [
        (jump_to_menu, "mnu_seven_ash_siege_warning"),
      ]),
      ("seven_ash_sector_back", [], "Return to the council map.", [
        (jump_to_menu, "mnu_seven_ash_oath_council"),
      ]),
    ]
  ),
]

