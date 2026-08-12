MENUS = [
(
    "past_life_explanation", mnf_disable_all_keys,
    "{s3}",
    "none",
    [
     # This menu is only valid for the five character-background paragraphs.
     # A stale global (including one carried by an old save) must not select an
     # arbitrary engine string register.
     (try_begin),
       (lt, "$current_string_reg", 10),
       (assign, "$current_string_reg", 10),
     (else_try),
       (gt, "$current_string_reg", 14),
       (assign, "$current_string_reg", 10),
     (try_end),
     # Keep the register selection explicit.  Besides hardening the runtime
     # path, this gives the DevKit a complete, auditable source set.
     (try_begin),
       (eq, "$current_string_reg", 10),
       (str_store_string_reg, s3, s10),
     (else_try),
       (eq, "$current_string_reg", 11),
       (str_store_string_reg, s3, s11),
     (else_try),
       (eq, "$current_string_reg", 12),
       (str_store_string_reg, s3, s12),
     (else_try),
       (eq, "$current_string_reg", 13),
       (str_store_string_reg, s3, s13),
     (else_try),
       (str_store_string_reg, s3, s14),
     (try_end),
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
