MENUS = [
(
    "encounter_retreat_confirm", mnf_enable_hot_keys,
    "As the party member with the highest tactics skill, ({reg2}), {reg3?you devise:{s3} devises} a plan that will allow you and your men to escape with your lives, but you'll have to leave {reg4} soldiers behind to stop the enemy from giving chase.",
    "none",
    [
      (set_background_mesh, "mesh_pic_retreat"),

      (call_script, "script_get_max_skill_of_player_party", "skl_tactics"),
      (assign, ":max_skill", reg0),
      (assign, ":max_skill_owner", reg1),
      (assign, reg2, ":max_skill"),
      (val_add, ":max_skill", 4),

      (call_script, "script_party_count_members_with_full_health", "p_collective_enemy", 0),
      (assign, ":enemy_party_strength", reg0),
      (val_div, ":enemy_party_strength", 2),

      (store_div, reg4, ":enemy_party_strength", ":max_skill"),
      (val_max, reg4, 1),

      (try_begin),
        (eq, ":max_skill_owner", "trp_player"),
        (assign, reg3, 1),
      (else_try),
        (assign, reg3, 0),
        (call_script, "script_store_troop_name", s3, ":max_skill_owner"),
      (try_end),
      ],
    [
      ("leave_behind", [], "Go on. The sacrifice of these men will save the rest.",
        [
          (assign, ":num_casualties", reg4),
          (try_for_range, ":unused", 0, ":num_casualties"),
            (call_script, "script_cf_party_remove_random_regular_troop", "p_main_party"),
            (assign, ":lost_troop", reg0),
            (store_random_in_range, ":random_no", 0, 100),
            (ge, ":random_no", 30),
            (party_add_prisoners, "$g_encountered_party", ":lost_troop", 1),
           (try_end),
           (call_script, "script_change_player_party_morale", -20),
           (jump_to_menu, "mnu_encounter_retreat"),
        ]),

      ("dont_leave_behind", [], "No. We leave no one behind.", [(jump_to_menu, "mnu_simple_encounter"), ]),
    ]
  ),
]
