MENUS = [
("runtime_sanity_report", mnf_enable_hot_keys,
   "{s20}",
   "none",
   [
     (set_background_mesh, "mesh_pic_report_screen"),
     (try_begin),
       (neq, "$cheat_mode", 1),
       (neq, "$g_sod_cheat_mode", 1),
       (jump_to_menu, "mnu_reports"),
     (try_end),
     (call_script, "script_sod_describe_runtime_sanity_to_s20"),
   ],
   [
     ("runtime_sanity_scrub", [
        (this_or_next|eq, "$cheat_mode", 1),
        (eq, "$g_sod_cheat_mode", 1),
      ], "Debug: clean stale encounter state.",
      [
        (call_script, "script_sod_sanitize_encounter_globals"),
        (display_message, "@Runtime sanity: stale encounter globals have been checked and cleared where invalid.", good_color),
        (jump_to_menu, "mnu_runtime_sanity_report"),
      ]),
     ("runtime_sanity_back", [], "Back to reports.",
      [
        (jump_to_menu, "mnu_reports"),
      ]),
   ]),
]
