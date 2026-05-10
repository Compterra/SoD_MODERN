MENUS = [
(
    "seven_ash_oswin_quarry", mnf_disable_all_keys,
    "Harrowcut Quarry smells of wet lime, rope fiber, and blame. The broken bridge lies below with its center span folded like a snapped rib. Oswin Ditchwright does not look up from the stone wedge in his hand until a worker mutters that the reeve never paid for proper pins.^^This menu frames the inspection; the recruitment choice belongs to dialogue with Oswin and the workers.",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_w"),
      (str_store_party_name, s11, "p_village_4"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_oswin_evidence, sod_seven_ash_evidence_physical),
    ],
    [
      ("seven_ash_oswin_talk", [
        (eq, "$current_town", "p_village_4"),
      ], "Inspect the bridge and speak with Oswin.", [
        (start_map_conversation, "trp_seven_ash_oswin_ditchwright"),
      ]),
      ("seven_ash_oswin_travel_needed", [
        (neq, "$current_town", "p_village_4"),
      ], "Travel to {s11}; Oswin is not here.", [
        (jump_to_menu, "mnu_start_phase_2"),
      ]),
      ("seven_ash_oswin_back", [], "Return to the recruitment board.", [
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

