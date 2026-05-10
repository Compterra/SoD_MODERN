MENUS = [
(
    "castle_siege_confirm", mnf_enable_hot_keys,
    "Are you certain you wish to provoke the {s1} into war?!",
    "none",
    [
      (set_background_mesh, "$g_sod_town_background"),
      (str_store_faction_name, s1, "$g_encountered_party_faction"),
    ],
    [
      ("castle_sige_confirm_war", [], "Yes, declare war!",
        [
          # declare war upon them, and begin the siege
          (assign, "$g_player_besiege_town", "$g_encountered_party"),
          (call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -10),   # Sod Twan (when player faction is active any attack start full war not only sieges)
##          (store_relation, ":relation", "fac_player_supporters_faction", "$g_encountered_party_faction"),
##          (assign, ":relation", -40),
##          (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":relation"),
##          (call_script, "script_update_all_notes"),                                                    # Sod Twan ends
          (jump_to_menu, "mnu_castle_besiege"),
        ]),

      ("castle_siege_confirm_not", [], "No, this is not the right time.", [(jump_to_menu, "mnu_castle_outside")]),
    ]
  ),
]
