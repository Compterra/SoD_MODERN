MENUS = [
("guilds_relations_report", mnf_enable_hot_keys,
   "{s1}",
   "none",
   [
    (set_background_mesh, "mesh_pic_report_screen"),
    (store_relation, ":cur_relation", "fac_player_supporters_faction", "fac_commoners"),
    (call_script, "script_get_realtion_name_s3", ":cur_relation"),
    (assign, reg1, ":cur_relation"),
    (str_store_string, s2, "@^The Commoners: {reg1} ({s3})"),
    (try_for_range, ":cur_kingdom", guilds_begin, guilds_end),
      (store_relation, ":cur_relation", "fac_player_supporters_faction", ":cur_kingdom"),
      (call_script, "script_get_realtion_name_s3", ":cur_relation"),
      (str_store_faction_name, s4, ":cur_kingdom"),
      (call_script, "script_merc_describe_guild_progression", ":cur_kingdom"),
      (assign, reg1, ":cur_relation"),
      (str_store_string, s2, "@{s2}^{s4}: {reg1} ({s3}) - {s64} {s65} {s66}"),
    (try_end),

    (str_store_string, s1, "@A tally of your standing with the guilds:^^Progression guide: promotion at 10, elite access by guild, special service at 30, trusted favor at 40.^{s2}"),                           # SoD twan end
    ],
    [
      ("continue", [], "Return to the reports...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
]
