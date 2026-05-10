MENUS = [
(
    "past_life_explanation", mnf_disable_all_keys,
    "{s3}",
    "none",
    [
     (try_begin),
       (gt, "$current_string_reg", 14),
       (assign, "$current_string_reg", 10),
     (try_end),
     (str_store_string_reg, s3, "$current_string_reg"),
     (try_begin),
       (ge, "$current_string_reg", 14),
       (str_store_string, s5, "@Back to the beginning..."),
     (else_try),
       (str_store_string, s5, "@View next segment..."),
     (try_end),
     ],
    [
      ("view_next", [], "{s5}", [
        (val_add, "$current_string_reg", 1),
        (jump_to_menu, "mnu_past_life_explanation"),
        ]),
      ("continue", [], "Continue...",
       [
        ]),
      ("go_back_dot", [], "Go back.", [
        (jump_to_menu, "mnu_choose_skill"),
        ]),
    ]
  ),
]
