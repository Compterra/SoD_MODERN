MENUS = [
("camp_action_read_book_start", mnf_scale_picture|mnf_enable_hot_keys,
   "{s1}",
   "none",
   [
    (set_background_mesh, "mesh_pic_camp"),
    (assign, ":new_book", "$temp"),
    (str_store_item_name, s2, ":new_book"),
    (try_begin),
      (store_attribute_level, ":int", "trp_player", ca_intelligence),
      (item_get_slot, ":int_req", ":new_book", slot_item_intelligence_requirement),
      (le, ":int_req", ":int"),
      (str_store_string, s1, "@You start reading {s2}. After a few pages, you feel you could learn a lot from this book. You decide to keep it close by and read whenever you have the time."),
      (assign, "$g_player_reading_book", ":new_book"),
    (else_try),
      (str_store_string, s1, "@You flip through the pages of {s2}, but you find the text confusing and difficult to follow. Try as you might, it soon gives you a headache, and you're forced to give up the attempt."),
    (try_end), ],
    [
      ("continue", [], "Continue...",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
]
