MENUS = [
(
    "seven_ash_siege_warning", mnf_disable_all_keys,
    "Nell Harrow comes back through the north ditch before dawn, mud to the knee and no breath wasted. Her tally is not a single host. Wulfred has bought deserters, hired road brigands, let Rafe bully fence-sitters into the column, and let Maud Ledger stretch it with wagons enough for a longer fight. Against your visible field strength, the scouts count roughly {reg0} attackers, with {reg1} hardened fighters held for the breach.",
    "none",
    [
      (set_background_mesh, "mesh_pic_siege_sighted"),
      (call_script, "script_party_count_fit_for_battle", "p_main_party", 0),
      (assign, ":player_field_strength", reg0),
      (call_script, "script_sod_seven_ash_compute_host_strength", ":player_field_strength"),
    ],
    [
      ("seven_ash_hear_nell_report", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_sector_commitment_locked, 1),
        (neg|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_final_plan, sod_seven_ash_plan_none),
      ], "Hear Nell's final scout report.", [
        (start_map_conversation, "trp_seven_ash_nell_harrow"),
      ]),
      ("seven_ash_begin_outer_fields", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_sector_commitment_locked, 1),
        (neg|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_final_plan, sod_seven_ash_plan_none),
      ], "Move to the outer fields.", [
        (jump_to_menu, "mnu_seven_ash_outer_fields"),
      ]),
      ("seven_ash_return_to_sector_commitment", [], "Return to the council map.", [
        (jump_to_menu, "mnu_seven_ash_sector_commitment"),
      ]),
    ]
  ),
]

