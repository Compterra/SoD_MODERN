MENUS = [
(
    "seven_ash_end_recruitment_confirm", mnf_disable_all_keys,
    "Closing the search will mark every unresolved defender road as abandoned. The people not found now may still matter later, but Act II will end and Ashwick will judge the return by who stands beside you.",
    "none",
    [
      (set_background_mesh, "mesh_pic_siege_sighted"),
      (quest_get_slot, ":resolved", "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_resolved_count),
      (assign, reg1, ":resolved"),
    ],
    [
      ("seven_ash_confirm_end_recruitment", [
        (ge, reg1, 3),
      ], "End the search and return to Ashwick.", [
        (call_script, "script_sod_seven_ash_close_recruitment"),
        (jump_to_menu, "mnu_seven_ash_return_to_ashwick"),
      ]),
      ("seven_ash_cancel_end_recruitment", [], "Keep searching.", [
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
    ]
  ),
]

