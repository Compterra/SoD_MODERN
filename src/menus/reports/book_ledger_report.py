try:
    from header_common import *  # noqa: F401,F403
    from header_operations import *  # noqa: F401,F403
except ImportError:
    pass

for _name in (
    "mnf_enable_hot_keys",
    "set_background_mesh",
    "call_script",
    "jump_to_menu",
    "s20",
):
    if _name not in globals():
        globals()[_name] = 0

MENUS = [
("book_ledger_report", mnf_enable_hot_keys,
   "{s20}",
   "none",
   [
      (set_background_mesh, "mesh_pic_report_screen"),
      (call_script, "script_sod_books_describe_library_report_to_s20"),
   ],
   [
      ("continue", [], "Continue...", [(jump_to_menu, "mnu_reports")]),
   ]
 ),
]
