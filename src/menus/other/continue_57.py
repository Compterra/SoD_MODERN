MENUS = [
(
    "kingdom_army_follow_failed", mnf_scale_picture,
    "You have disobeyed orders and failed to follow {s8}. In anger he has disbanded you from the army, and sends a stern warning that your actions will not be forgotten.",
    "none",
    [
      (set_background_mesh, "mesh_pic_messenger"),
      (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
      (call_script, "script_store_troop_name", s8, ":faction_marshall"),
      (try_begin),
        (check_quest_active, "qst_follow_army"),
        (call_script, "script_abort_quest", "qst_follow_army", 1),
        (call_script, "script_change_player_relation_with_troop", ":faction_marshall", -3),
      (try_end),
    ],
    [
      ("continue", [], "Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
]
