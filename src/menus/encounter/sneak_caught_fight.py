MENUS = [
(
    "sneak_into_town_caught", 0,
    "As you try to sneak in, one of the guards recognizes you and raises the alarm! You must flee back through the gates before all the guards in the town come down on you!",
    "none",
    [
      (set_background_mesh, "$g_sod_town_background"),
      (assign, "$auto_menu", "mnu_captivity_start_castle_surrender"),
    ],
    [
      ("sneak_caught_fight", [], "Try to fight your way out!",
        [
          (assign, "$all_doors_locked", 1),
          (party_get_slot, ":sneak_scene", "$current_town", slot_town_center), # slot_town_gate),
          (modify_visitors_at_site, ":sneak_scene"), (reset_visitors),
          (set_visitor, 0, "trp_player"),
          (store_faction_of_party, ":town_faction", "$current_town"),
          (faction_get_slot, ":tier_2_troop", ":town_faction", slot_faction_tier_2_troop),
          (faction_get_slot, ":tier_3_troop", ":town_faction", slot_faction_tier_3_troop),
          (try_begin),
            (gt, ":tier_2_troop", 0),
            (gt, ":tier_3_troop", 0),
            (assign, reg(0), ":tier_3_troop"),
            (assign, reg(1), ":tier_3_troop"),
            (assign, reg(2), ":tier_2_troop"),
            (assign, reg(3), ":tier_2_troop"),
          (else_try),
            (assign, reg(0), "trp_swadian_skirmisher"),
            (assign, reg(1), "trp_swadian_crossbowman"),
            (assign, reg(2), "trp_swadian_infantry"),
            (assign, reg(3), "trp_swadian_crossbowman"),
          (try_end),
          (assign, reg(4), -1),
          (shuffle_range, 0, 5),
          (set_visitor, 1, reg(0)),
          (set_visitor, 2, reg(1)),
          (set_visitor, 3, reg(2)),
          (set_visitor, 4, reg(3)),
          (set_jump_mission, "mt_sneak_caught_fight"),
          (set_passage_menu, "mnu_town"),
          (jump_to_scene, ":sneak_scene"),
          (change_screen_mission),
        ]
      ),

      ("sneak_caught_surrender", [], "Surrender.", [ (jump_to_menu, "mnu_captivity_start_castle_surrender"), ]),
    ]
  ),
]
