MENUS = [
("royal_reliquary_report", mnf_enable_hot_keys,
   "{s1}",
   "none",
  [
    (set_background_mesh, "mesh_pic_report_screen"),
    (call_script, "script_sod_artifact_describe_reliquary_report"),
    ],
    [
      ("inspect_artifacts", [], "Inspect and maintain royal artifacts.", [(jump_to_menu, "mnu_royal_artifact_smith"),]),
      ("continue", [], "Continue...", [(jump_to_menu, "mnu_reports"),]),
      ]
  ),
]
