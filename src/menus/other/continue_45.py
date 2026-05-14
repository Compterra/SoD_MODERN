MENUS = [
(
    "sneak_into_town_succeeded", 0,
    "Disguised in the garments of a poor pilgrim, you fool the guards and make your way into the town.",
    "none",
    [
      (set_background_mesh, "$g_sod_town_background"),
    ],
    [
      ("continue", [], "Continue...", [ (call_script, "script_sod_companion_retinue_repair_all"), (assign, "$sneaked_into_town", 1), (jump_to_menu, "mnu_town"), ] ),
    ]
  ),
]
