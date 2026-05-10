MENUS = [
(
    "seven_ash_pressure_board", mnf_disable_all_keys,
    "Ashwick's fear is no longer a rumor on the road. It is smoke in a pasture, knife cuts on doors, and shouting at the granary. Choose where to go; the decision belongs to the people waiting there.",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_w"),
    ],
    [
      ("seven_ash_pressure_burned_cow", [
        (quest_get_slot, ":resolved_bits", "qst_seven_ash_ultimatum", slot_quest_seven_ash_pressure_interlude_resolved_bits),
        (store_and, ":done", ":resolved_bits", sod_seven_ash_interlude_burned_cow),
        (eq, ":done", 0),
      ], "Go to the burned cow at the outer pasture.", [
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_pressure_interlude_active, sod_seven_ash_interlude_burned_cow),
        (start_map_conversation, "trp_seven_ash_mother_hilda"),
      ]),
      ("seven_ash_pressure_knife_marked_door", [
        (quest_get_slot, ":resolved_bits", "qst_seven_ash_ultimatum", slot_quest_seven_ash_pressure_interlude_resolved_bits),
        (store_and, ":done", ":resolved_bits", sod_seven_ash_interlude_knife_marked_door),
        (eq, ":done", 0),
      ], "Go to the knife-marked door.", [
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_pressure_interlude_active, sod_seven_ash_interlude_knife_marked_door),
        (start_map_conversation, "trp_seven_ash_nell_harrow"),
      ]),
      ("seven_ash_pressure_grain_riot", [
        (quest_get_slot, ":resolved_bits", "qst_seven_ash_ultimatum", slot_quest_seven_ash_pressure_interlude_resolved_bits),
        (store_and, ":done", ":resolved_bits", sod_seven_ash_interlude_grain_riot),
        (eq, ":done", 0),
      ], "Go to the granary before the line breaks.", [
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_pressure_interlude_active, sod_seven_ash_interlude_grain_riot),
        (start_map_conversation, "trp_seven_ash_reeve_martin"),
      ]),
      ("seven_ash_pressure_wulfred_offer", [
        (quest_get_slot, ":resolved_bits", "qst_seven_ash_ultimatum", slot_quest_seven_ash_pressure_interlude_resolved_bits),
        (store_and, ":done", ":resolved_bits", sod_seven_ash_interlude_wulfred_offer),
        (eq, ":done", 0),
        (quest_get_slot, ":recruited", "qst_seven_ash_ultimatum", slot_quest_seven_ash_recruited_bitmask),
        (gt, ":recruited", 0),
      ], "Read Wulfred's offer before the village.", [
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_pressure_interlude_active, sod_seven_ash_interlude_wulfred_offer),
        (start_map_conversation, "trp_seven_ash_rafe_carrick"),
      ]),
      ("seven_ash_pressure_first_funeral", [
        (quest_get_slot, ":resolved_bits", "qst_seven_ash_ultimatum", slot_quest_seven_ash_pressure_interlude_resolved_bits),
        (store_and, ":done", ":resolved_bits", sod_seven_ash_interlude_first_funeral),
        (eq, ":done", 0),
      ], "Stand at the first funeral before the siege.", [
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_pressure_interlude_active, sod_seven_ash_interlude_first_funeral),
        (start_map_conversation, "trp_seven_ash_mother_hilda"),
      ]),
      ("seven_ash_pressure_call_oath_council", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_final_plan, sod_seven_ash_plan_none),
        (quest_get_slot, ":resolved_bits", "qst_seven_ash_ultimatum", slot_quest_seven_ash_pressure_interlude_resolved_bits),
        (gt, ":resolved_bits", 0),
      ], "Call the Oath Council in the church.", [
        (jump_to_menu, "mnu_seven_ash_oath_council"),
      ]),
      ("seven_ash_pressure_back", [], "Return to Ashwick's preparations.", [
        (jump_to_menu, "mnu_start_phase_2"),
      ]),
    ]
  ),
]

