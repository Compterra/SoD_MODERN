MENUS = [
(
    "kingdom_army_quest_messenger", mnf_scale_picture,
    "{s8} sends word that he wishes to speak with you about a task he needs performed. He requests you to come and see him as soon as possible.",
    "none",
    [
      (set_background_mesh, "mesh_pic_messenger"),
      (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
      (call_script, "script_store_troop_name", s8, ":faction_marshall"),
    ],
    [
      ("continue", [], "Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
]
