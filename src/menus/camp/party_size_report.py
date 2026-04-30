MENUS = [
("party_size_report", mnf_enable_hot_keys,
   "{s1}",
   "none",
   [
    (set_background_mesh, "mesh_pic_report_screen"),
    (call_script, "script_game_get_party_companion_limit"),
    (assign, ":party_size_limit", reg0),

    (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
    #MORDACHAI - Leadership counts x10 (was x5)
    (val_mul, ":leadership", 10),
    (store_attribute_level, ":charisma", "trp_player", ca_charisma),

    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (val_div, ":renown", 25),
    (try_begin),
      (gt, ":leadership", 0),
      (str_store_string, s2, "@ +"),
    (else_try),
      (str_store_string, s2, "@ "),
    (try_end),
    (try_begin),
      (gt, ":charisma", 0),
      (str_store_string, s3, "@ +"),
    (else_try),
      (str_store_string, s3, "@ "),
    (try_end),
    (try_begin),
      (gt, ":renown", 0),
      (str_store_string, s4, "@ +"),
    (else_try),
      (str_store_string, s4, "@ "),
    (try_end),
    (assign, reg5, ":party_size_limit"),
    (assign, reg1, ":leadership"),
    (assign, reg2, ":charisma"),
    (assign, reg3, ":renown"),
    (str_store_string, s1, "@Current party size limit is {reg5}.^Current party size modifiers are:^^Base size:  +10^Leadership: {s2}{reg1}^Charisma: {s3}{reg2}^Renown: {s4}{reg3}^TOTAL:  {reg5}"),
    ],
    [
      ("continue", [], "Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
]
