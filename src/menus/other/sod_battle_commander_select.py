MENUS = [
(
    "sod_battle_commander_select", 0,
    "Choose who will lead the next fight. Current acting commander: {s7}. If you cannot fight, select a fit companion.",
    "none",
    [
      (set_background_mesh, "mesh_pic_attack_ready"),
      (call_script, "script_sod_battle_commander_store_current_name_to_s7"),
    ],
    generate_sod_battle_commander_select_options()
  ),
]
