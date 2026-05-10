MENUS = [
(
    "castle_guard", mnf_enable_hot_keys,
    "You approach the gate. The men on the walls watch you closely.",
    "none",
    [
      (set_background_mesh, "$g_sod_town_background"),
    ],
    [
      ("request_shelter", [(party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
                          (ge, "$g_encountered_party_relation", 0)],
       "Request entry to the castle.",
       [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
        (try_begin),
          (lt, ":castle_lord", 0),
          (jump_to_menu, "mnu_castle_entry_granted"),
        (else_try),
          #MORDACHAI - grant King access always
          (eq, "$g_encountered_party_faction", "$players_kingdom"),
          (faction_slot_eq, "$g_encountered_party_faction", slot_faction_leader, "trp_player"),
          (jump_to_menu, "mnu_castle_entry_granted"),
        (else_try),
          (call_script, "script_troop_get_player_relation", ":castle_lord"),
          (assign, ":castle_lord_relation", reg0),
          (try_begin),
            (gt, ":castle_lord_relation", -15),
            (jump_to_menu, "mnu_castle_entry_granted"),
          (else_try),
            (jump_to_menu, "mnu_castle_entry_denied"),
          (try_end),
        (try_end),
       ]),
      ("request_meeting_commander", [],
       "Request a meeting with someone.",
       [
          (jump_to_menu, "mnu_castle_meeting"),
       ]),
      ("guard_leave", [],
       "Leave.",
       [(change_screen_return, 0)]),
    ]
  ),
]
