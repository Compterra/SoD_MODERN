MENUS = [
(
    "seven_ash_village_audit", mnf_disable_all_keys,
    "{s1}^^{s2}^^{s3}^^{s4}^^{s5}^^Ashwick is not a fortress. It is a place with a ditch that wants to be a wall, a churchyard that may become a last line, dry cellars that may become either shelter or traps, and families who still call the outer farms home.",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_p"),
      (quest_get_slot, ":posture", "qst_seven_ash_ultimatum", slot_quest_sod_chain_choice),
      (quest_get_slot, ":pressure", "qst_seven_ash_ultimatum", slot_quest_seven_ash_wulfred_pressure),

      (try_begin),
        (eq, ":posture", sod_seven_ash_method_common_defense),
        (str_store_string, s1, "@Mother Hilda starts with names, not walls: the old, the fevered, the children too small to run."),
      (else_try),
        (eq, ":posture", sod_seven_ash_posture_find_defenders),
        (str_store_string, s1, "@Nell names destroyed villages before she names possible defenders. She wants you to understand the price of arriving late."),
      (else_try),
        (eq, ":posture", sod_seven_ash_posture_lordly_aid),
        (str_store_string, s1, "@Reeve Martin folds the lord's letter twice, as if a sharper crease could make help arrive sooner."),
      (else_try),
        (eq, ":posture", sod_seven_ash_method_wulfred_bargain),
        (str_store_string, s1, "@The word bargain has already soured the square. Everyone knows tribute is just fear with a clerk."),
      (else_try),
        (eq, ":posture", sod_seven_ash_posture_evacuate),
        (str_store_string, s1, "@Piers counts carts, axles, mules, and which families will lie about being ready to leave."),
      (else_try),
        (str_store_string, s1, "@Ashwick waits for a first task, because waiting by itself has begun to feel like surrender."),
      (try_end),

      (try_begin),
        (ge, ":pressure", 25),
        (str_store_string, s2, "@Wulfred's pressure is already high. Killing or silencing messengers bought pride, not time."),
      (else_try),
        (str_store_string, s2, "@Wulfred's riders are gone for now. Their hoofprints still point both ways."),
      (try_end),

      (str_store_string, s3, "@At the palisade, rotten posts shift under one hand. At the granary, the keys sound louder than coins. At the churchyard, the stone wall is low but honest."),
      (str_store_string, s4, "@At the mill bridge, Piers names the ford a raider would try first. At the outer farms, Nell says Wulfred always leaves one witness alive."),
      (str_store_string, s5, "@Under the church and three old houses, the cellars stay dry. Mother Hilda says they can hold wounded, children, grain, or terrified silence, but not all at once."),
    ],
    [
      ("seven_ash_hear_audit_witnesses", [], "Hear the village witnesses before choosing the first priority.", [
        (jump_to_menu, "mnu_seven_ash_village_audit_witnesses"),
      ]),
    ]
  ),

(
    "seven_ash_village_audit_witnesses", mnf_disable_all_keys,
    "Mother Hilda starts with people: 'The old cannot run, the fevered cannot hide, and children do not become lighter because a captain is hurried.'^^Reeve Martin holds up the granary key: 'Food is time. Spend it badly and Wulfred need not breach anything.'^^Piers Wainwright names carts, axles, mules, and the ford by the mill: 'A road saves only the families it reaches before smoke does.'^^Nell of Little Harrow points past the ditch: 'Scouts do not stop a wolf. They tell you which door he sniffs first.'^^Now the village waits for a spoken order that will make one fear heavier than the rest.",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_p"),
    ],
    [
      ("seven_ash_priority_palisade", [], "Reeve, pull timber first. The palisade cannot stay a rumor.", [
        (call_script, "script_sod_seven_ash_choose_audit_priority", sod_seven_ash_priority_repair_palisade),
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
      ("seven_ash_priority_ditch", [], "Dig the ditch and stake the approaches. Make the ground fight for us.", [
        (call_script, "script_sod_seven_ash_choose_audit_priority", sod_seven_ash_priority_dig_ditch),
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
      ("seven_ash_priority_granary", [], "Lock the granary under witness. Hunger will not command this village first.", [
        (call_script, "script_sod_seven_ash_choose_audit_priority", sod_seven_ash_priority_secure_granary),
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
      ("seven_ash_priority_militia", [], "Give me every spear, broom handle, and frightened adult. We drill before sunset.", [
        (call_script, "script_sod_seven_ash_choose_audit_priority", sod_seven_ash_priority_train_militia),
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
      ("seven_ash_priority_farms", [], "Piers, bring in the outer farms first. Homes can burn after people leave them.", [
        (call_script, "script_sod_seven_ash_choose_audit_priority", sod_seven_ash_priority_evacuate_farms),
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
      ("seven_ash_priority_scout", [], "Nell, show me Wulfred's road. I want eyes beyond the ditch.", [
        (call_script, "script_sod_seven_ash_choose_audit_priority", sod_seven_ash_priority_scout_road),
        (jump_to_menu, "mnu_seven_ash_recruitment_map"),
      ]),
      ("seven_ash_priority_back_to_audit", [], "Walk the village once more before deciding.", [
        (jump_to_menu, "mnu_seven_ash_village_audit"),
      ]),
    ]
  ),
]

